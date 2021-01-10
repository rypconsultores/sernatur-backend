from django.http import HttpResponse

from . import api


def root(request):
    return HttpResponse('')