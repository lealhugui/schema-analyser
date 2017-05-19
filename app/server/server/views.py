import os
import mimetypes

from django.apps import apps
from django.views.generic import View
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from django.http import JsonResponse, HttpResponse

from server.settings import BASE_DIR, DEBUG


class InterfaceView(View):

    """View that renders the UI client.
    """

    http_method_names = ['get', ]    

    @staticmethod
    def statics(request, path):

        mimetypes.init()

        if len(path)==0:
            path = "index.html"

        file_handler = os.path.join(
            BASE_DIR,
            'client',
            'build',
            path)

        file_name, file_extension = os.path.splitext(path)

        mimetype = "plain/text"
        try:
            mimetype = mimetypes.types_map[file_extension]
        except Exception:
            pass
        req_file = open(file_handler, 'rb')
        return HttpResponse(content=req_file.read(), content_type=mimetype)
