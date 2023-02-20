import json

from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Request, Response


class WSGIApplication(object):
    def __init__(self, name):
        self.name = name
        self.url_map = Map([])

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)

    def dispatch(self, environ, start_response):
        request = Request(environ)
        data = self.extract_json(request)
        url_adapter = self.url_map.bind_to_environ(request.environ)
        endpoint, values = url_adapter.match()
        response = Response(endpoint(request=request, data=data))

        return response(environ, start_response)

    def mapping(self, url, **options):
        def decorator(f):
            self.url_map.add(Rule(url, endpoint=f))
            print(url, options)
            print(f)
            return f

        return decorator

    def extract_json(self, request):
        data = None
        if request.content_type == 'application/json':
            data = json.loads(request.get_data().decode('utf-8'))
        return data
