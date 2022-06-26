from starlette.routing import compile_path
import typing
from starlette.datastructures import URL, Headers, URLPath
from starlette.routing import NoMatchFound, replace_params


class Route:

    # Modified code from Starlette routing.py: https://github.com/encode/starlette/blob/master/starlette/routing.py
    # Copyright © 2018, Encode OSS Ltd. All rights reserved.
    # You may obtain a copy of the License at: https://github.com/encode/starlette/blob/master/LICENSE.md

    instances = []
    id = 0

    def __init__(self, path: str, func_to_run: typing.Callable, last=False, **kwargs):

        assert path.startswith("/"), "Routed paths must start with '/'"
        self.path = path
        self.func_to_run = func_to_run
        self.name = kwargs.get('name', None)
        self.path_regex, self.path_format, self.param_convertors = compile_path(path)
        self.id = Route.id
        Route.id += 1
        if last:
            Route.instances.append(self)
        else:
            Route.instances.insert(0, self)

    def matches(self, path, request):
        match = self.path_regex.match(path)
        if match:
            matched_params = match.groupdict()
            for key, value in matched_params.items():
                matched_params[key] = self.param_convertors[key].convert(value)
            request.path_params.update(matched_params)
            return self.func_to_run
        else:
            return False

    def __repr__(self):
        return f'{self.__class__.__name__}(name: {self.name}, id: {self.id}, path: {self.path}, format: {self.path_format}, func: {self.func_to_run.__name__}, regex: {self.path_regex})'

    @classmethod
    def url_for(cls, name: str, **path_params: typing.Any) -> URLPath:
        for route in cls.instances:
            try:
                return route.url_path_for(name, **path_params)
            except NoMatchFound:
                pass
        raise NoMatchFound(name, path_params)

    
    def url_path_for(self, name: str, **path_params: typing.Any) -> URLPath:
        print("searching for path ", self.name)
        if self.name is not None and name == self.name:
            # 'name' matches "<mount_name>".
            print ("building urlpath for ", self.path)
            return URLPath(path=self.path)
            
        if self.name is not None and name == self.name and "path" in path_params:
            # 'name' matches "<mount_name>".
            path_params["path"] = path_params["path"].lstrip("/")
            path, remaining_params = replace_params(
                self.path_format, self.param_convertors, path_params
            )
            if not remaining_params:
                return URLPath(path=path)
        elif self.name is None or name.startswith(self.name + ":"):
            if self.name is None:
                # No mount name.
                remaining_name = name
            else:
                # 'name' matches "<mount_name>:<child_name>".
                remaining_name = name[len(self.name) + 1 :]
            path_kwarg = path_params.get("path")
            path_params["path"] = ""
            path_prefix, remaining_params = replace_params(
                self.path_format, self.param_convertors, path_params
            )
            if path_kwarg is not None:
                remaining_params["path"] = path_kwarg
            for route in self.routes or []:
                try:
                    url = Route.url_path_for(remaining_name, **remaining_params)
                    return URLPath(
                        path=path_prefix.rstrip("/") + str(url), protocol=url.protocol
                    )
                except NoMatchFound:
                    pass
        raise NoMatchFound(name, path_params)

class SetRoute:

    def __init__(self, route, **kwargs):
        self.route = route
        self.kwargs = kwargs


    def __call__(self, fn, **kwargs):
        Route(self.route, fn,  name=self.kwargs.get('name', None))
        return fn


