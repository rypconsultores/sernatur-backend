from django.http import HttpResponse


def skeretonu(request):
    return HttpResponse(
        "<html><head>"
        "<style>body,html{font-family:Arial,helvetica,sans-serif;}</style>"
        "</head><body><h1>Hero skeretonu!</h1></body>"
    )