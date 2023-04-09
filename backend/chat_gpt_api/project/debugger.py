from django.conf import settings
import json


class DebugMe:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ignoreP = ["static"]

        if request.path.split("/")[1] not in ignoreP:
            if settings.DEBUG:
                r = json.dumps("%s" % request.__dict__, sort_keys=True, indent=4)
                print(r)

        response = self.get_response(request)

        return response
