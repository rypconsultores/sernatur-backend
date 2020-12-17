from collections.abc import Mapping as MappingBase
from typing import Any, Sequence, Mapping, List, Dict

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Empty, Request

from ... import models, serializers


class PlacePersonCheckViewSet(
    mixins.ListModelMixin, mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    serializer_class = serializers.PlacePersonCheck
    queryset = models.PlacePersonCheck.objects
    permission_classes = [IsAuthenticated]

    def initialize_request(
        self, *args: List[Any], **kwargs: Dict[str, Any]
    ):
        request: Request = super().initialize_request(*args, **kwargs)

        # Force parsing of data
        request.data

        if 'id_place' in kwargs and request._full_data is not Empty:
            data: Mapping[str, Any]
            data_list: Sequence[Mapping[str, Any]]

            if isinstance(request._full_data, list):
                data_list = request._full_data
            else:
                data_list = [request._full_data]

            if hasattr(request.data, '_mutable'):
                request.data._mutable = True

            for i, data in enumerate(data_list):
                if isinstance(data, str) and data.startswith('{') and data.endswith('}'):
                    data_list[i] = f'{{"place_id":{kwargs["id_place"]},{data[1:]}'
                else:
                    if not isinstance(data, MappingBase):
                        raise ValueError("Not a dict based data: %s" % (repr(data),))

                    data['place_id'] = kwargs['id_place']

        return request
