from django.http import HttpResponse
import json


class BaseView(object):
    def __call__(self, request, *args, **kwargs):
        method_name = request.method.strip().lower()
        method = getattr(self, method_name, None)
        if method:
            return method(request, *args, **kwargs)
        else:
            return HttpResponse(status=405)

    def render(self, data={}, **kwargs):
        data.update(kwargs)
        return HttpResponse(content=json.dumps(data))


