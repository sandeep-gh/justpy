from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse, Response
from starlette.responses import PlainTextResponse
from starlette.endpoints import WebSocketEndpoint
from starlette.endpoints import HTTPEndpoint
from starlette.middleware import Middleware
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.staticfiles import StaticFiles
from justpy.htmlcomponents import *
from .chartcomponents import *
from .gridcomponents import *
from .quasarcomponents import *

from jpcore.justpy_app import cookie_signer, template_options, handle_event, JustpyApp,JustpyAjaxEndpoint
import jpcore.jpconfig as jpconfig
from jpcore.justpy_config import JpConfig
JustPy.LOGGING_LEVEL = jpconfig.LOGGING_LEVEL
# from .misccomponents import *
from .pandas import *

from jpcore.utilities import run_task, create_delayed_task
import uvicorn, logging, sys, os, traceback
import typing
#
# globals
#
# uvicorn Server
jp_server = None
current_module = sys.modules[__name__]
current_dir = os.path.dirname(current_module.__file__)
if jpconfig.VERBOSE:
    print(current_dir.replace("\\", "/"))
    print(f"Module directory: {current_dir}, Application directory: {os.getcwd()}")

logging.basicConfig(level=jpconfig.LOGGING_LEVEL, format="%(levelname)s %(module)s: %(message)s")

def build_app(middlewares=None, APPCLASS = JustpyApp, startup_func = None):
    if not middlewares:
        middlewares = []
    middlewares.append(Middleware(GZipMiddleware))
    if jpconfig.SSL_KEYFILE and jpconfig.SSL_CERTFILE:
        middlewares.append(Middleware(HTTPSRedirectMiddleware))
    
    #@TODO     
    # implement https://github.com/justpy-org/justpy/issues/535
    #if SESSIONS:
    #    middleware.append(Middleware(SessionMiddleware, secret_key=SECRET_KEY))
    app = APPCLASS(middleware=middlewares, debug=jpconfig.DEBUG)
    assert app is not None
    app.mount(jpconfig.STATIC_ROUTE, StaticFiles(directory=jpconfig.STATIC_DIRECTORY), name=jpconfig.STATIC_NAME)
    app.mount(
        "/templates", StaticFiles(directory=current_dir + "/templates"), name="templates"
    )

    @app.on_event("startup")
    async def justpy_startup():
        WebPage.loop = asyncio.get_event_loop()
        JustPy.loop = WebPage.loop
        JustPy.STATIC_DIRECTORY = jpconfig.STATIC_DIRECTORY

        if startup_func:
            if inspect.iscoroutinefunction(startup_func):
                await startup_func()
            else:
                startup_func()
        protocol = "https" if jpconfig.SSL_KEYFILE else "http"
        print(f"JustPy ready to go on {protocol}://{jpconfig.HOST}:{jpconfig.PORT}")

    
    @app.route("/zzz_justpy_ajax")
    class AjaxEndpoint(JustpyAjaxEndpoint):
        """
        Justpy ajax handler
        """
    
    @app.websocket_route("/")
    class JustpyEvents(WebSocketEndpoint):

        socket_id = 0
        
        async def on_connect(self, websocket):
            await websocket.accept()
            websocket.id = JustpyEvents.socket_id
            websocket.open = True
            logging.debug(f"Websocket {JustpyEvents.socket_id} connected")
            JustpyEvents.socket_id += 1
            # Send back socket_id to page
            # await websocket.send_json({'type': 'websocket_update', 'data': websocket.id})
            WebPage.loop.create_task(
                websocket.send_json({"type": "websocket_update", "data": websocket.id})
            )

        async def on_receive(self, websocket, data):
            """
            Method to accept and act on data received from websocket
            """
            logging.debug("%s %s", f"Socket {websocket.id} data received:", data)
            data_dict = json.loads(data)
            msg_type = data_dict["type"]
            # data_dict['event_data']['type'] = msg_type
            if msg_type == "connect":
                # Initial message sent from browser after connection is established
                # WebPage.sockets is a dictionary of dictionaries
                # First dictionary key is page id
                # Second dictionary key is socket id
                page_key = data_dict["page_id"]
                websocket.page_id = page_key
                if page_key in WebPage.sockets:
                    WebPage.sockets[page_key][websocket.id] = websocket
                else:
                    WebPage.sockets[page_key] = {websocket.id: websocket}
                return
            if msg_type == "event" or msg_type == "page_event":
                # Message sent when an event occurs in the browser
                session_cookie = websocket.cookies.get(jpconfig.SESSION_COOKIE_NAME)
                if jpconfig.SESSIONS and session_cookie:
                    session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                    data_dict["event_data"]["session_id"] = session_id
                # await self._event(data_dict)
                data_dict["event_data"]["msg_type"] = msg_type
                page_event = True if msg_type == "page_event" else False
                WebPage.loop.create_task(
                    handle_event(data_dict, com_type=0, page_event=page_event)
                )
                return
            if msg_type == "zzz_page_event":
                # Message sent when an event occurs in the browser
                session_cookie = websocket.cookies.get(jpconfig.SESSION_COOKIE_NAME)
                if jpconfig.SESSIONS and session_cookie:
                    session_id = cookie_signer.unsign(session_cookie).decode("utf-8")
                    data_dict["event_data"]["session_id"] = session_id
                data_dict["event_data"]["msg_type"] = msg_type
                WebPage.loop.create_task(
                    handle_event(data_dict, com_type=0, page_event=True)
                )
                return

        async def on_disconnect(self, websocket, close_code):
            
            try:
                pid = websocket.page_id
            except:
                return
            websocket.open = False
            WebPage.sockets[pid].pop(websocket.id)
            if not WebPage.sockets[pid]:
                WebPage.sockets.pop(pid)
            await WebPage.instances[pid].on_disconnect(
                websocket
            )  # Run the specific page disconnect function
            if jpconfig.MEMORY_DEBUG:
                print("************************")
                print(
                    "Elements: ",
                    len(JustpyBaseComponent.instances),
                    JustpyBaseComponent.instances,
                )
                print("WebPages: ", len(WebPage.instances), WebPage.instances)
                print("Sockets: ", len(WebPage.sockets), WebPage.sockets)
                import psutil
                process = psutil.Process(os.getpid())
                print(f"Memory used: {process.memory_info().rss:,}")
                print("************************")

    return app

def initial_func(_request):
    """
    Default func/endpoint to be called if none has been specified
    """
    wp = WebPage()
    Div(
        text="JustPy says: Page not found",
        classes="inline-block text-5xl m-3 p-3 text-white bg-blue-600",
        a=wp,
    )
    return wp


func_to_run = initial_func



def server_error_func(request):
    wp = WebPage()
    Div(
        text="JustPy says: 500 - Server Error",
        classes="inline-block text-5xl m-3 p-3 text-white bg-red-600",
        a=wp,
    )
    return wp


def get_server():
    """
    Workaround for global variable jp_server not working as expected
    """
    return jp_server

def Route(path:str,wpfunc:typing.Callable):
    """
    legacy Route handling
    
    Args:
        path (str): the path of the route to add
        wpfunc(Callable): a WebPage returning function to be added
    """
    app.add_jproute(path,wpfunc)


# jp.justpy entry point is deprecated now.
# use uvicorn from command line
def launch_uvicorn_webserver(
        app,
        host: str = jpconfig.HOST,
        port: int = jpconfig.PORT,

):
    """
    """
   
    if jpconfig.SSL_KEYFILE and jpconfig.SSL_CERTFILE:
        uvicorn_config = uvicorn.config.Config(
            app,
            host=host,
            port=port,
            log_level=jpconfig.UVICORN_LOGGING_LEVEL,
            proxy_headers=True,
            ssl_keyfile=jpconfig.SSL_KEYFILE,
            ssl_certfile=jpconfig.SSL_CERTFILE,
            ssl_version=jpconfig.SSL_VERSION,
        )
    else:
        uvicorn_config = uvicorn.config.Config(
            app, host=host, port=port, log_level=jpconfig.UVICORN_LOGGING_LEVEL
        )
    jp_server = uvicorn.Server(uvicorn_config)
    jp_server.run()



def convert_dict_to_object(d):
    """
    convert the given dict to an object
    """
    obj = globals()[d["class_name"]]()
    for obj_prop in d["object_props"]:
        obj.add(convert_dict_to_object(obj_prop))
    # combine the dictionaries
    for k, v in {**d, **d["attrs"]}.items():
        if k != "id":
            obj.__dict__[k] = v
    return obj


def redirect(url:str)->WebPage:
    """
    redirect to the given url
    
    Args:
        url(str): the url to redirect to
        
    Returns:
        a WebPage with a single Div that hat the redirect
    """
    wp = WebPage()
    wp.add(Div())
    wp.redirect = url
    return wp
