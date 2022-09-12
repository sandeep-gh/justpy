# Justpy Tutorial demo hello_world from docs/tutorial/getting_started.md
import justpy as jp


def hello_world():
    wp = jp.WebPage()
    jp.Hello(a=wp)
    return wp


# initialize the demo
# from examples.basedemo import Demo

# Demo("hello_world", hello_world)
jp.Route("/", hello_world)
from starlette.testclient import TestClient
app = jp.app
client = TestClient(app)
response = client.get('/') 
