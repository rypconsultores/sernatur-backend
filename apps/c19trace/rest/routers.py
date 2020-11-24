from typing import Tuple, List, Optional, Any, Dict, Union

from rest_framework.routers import SimpleRouter, Route, DynamicRoute
from django.views import View


# (self, prefix, viewset, basename=None)
RouteArg = Union[
    Tuple[str, View, Optional[str]],
    Tuple[str, View]
]


class DefaultRouter(SimpleRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'list',
                'post': 'create'
            },
            name='{basename}.list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{url_path}{trailing_slash}$',
            name='{basename}.{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}.detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^{prefix}/{lookup}/{url_path}{trailing_slash}$',
            name='{basename}.{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]

    def __init__(
        self, routes: Optional[List[RouteArg]] = None, trailing_slash=True,
        *args: List[Any], **kwargs: Dict[str, Any]
    ):
        super().__init__(trailing_slash=trailing_slash, *args, **kwargs)

        if routes:
            route: RouteArg
            for route in routes:
                self.register(*route)