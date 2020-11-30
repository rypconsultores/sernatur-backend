from functools import wraps
from types import MethodType
from typing import Optional, List, Callable, Any, Dict

from django.http import HttpRequest, HttpResponse
from rest_framework.decorators import api_view as drf_api_view
from rest_framework.serializers import BaseSerializer

Function = Callable[..., Any]
Decorator = Callable[[Function], Function]


def nocsrf(view: Function) -> Function:
    @wraps(view)
    def nocsrf_view(
        request: HttpRequest,
        *args: List[Any], **kwargs: Dict[str, Any]
    ) -> HttpResponse:
        request._dont_enforce_csrf_checks = True
        return view(request, *args, **kwargs)

    return nocsrf_view


def api_view(
    http_method_names: Optional[List[str]] = None,
    use_serializer: Optional[BaseSerializer] = None
) -> Function:
    if use_serializer is None:
        return drf_api_view(http_method_names)

    def api_view_deco_wrap(view: Function) -> Function:
        nonlocal http_method_names, use_serializer

        decorated_view = drf_api_view(http_method_names)(view)

        if use_serializer:
            decorated_view.cls.get_serializer = \
                MethodType(lambda s: use_serializer(), decorated_view.cls)

        return decorated_view

    return api_view_deco_wrap
