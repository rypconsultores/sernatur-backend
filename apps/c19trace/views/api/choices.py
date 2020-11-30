from typing import Union, Callable, Tuple, Sequence

from django.http import JsonResponse, HttpResponse
from requests import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from ...util.api import api_view
from ... import serializers
from ...models import choices as choices_data

import json

from django.utils.functional import Promise
from django.utils.encoding import force_text
from django.core.serializers.json import DjangoJSONEncoder

ResponseType = Union[Response, HttpResponse]
ViewType = Callable[[Request], ResponseType]
ChoicesSet = Sequence[Tuple[Union[str, int], str]]


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        return super(LazyEncoder, self).default(obj)


def view_maker(choice_set: ChoicesSet, serializer: Serializer) -> ViewType:
    @api_view(["GET"], use_serializer=serializer)
    def _view(request):
        return JsonResponse(
            tuple(map(dict_choice, choice_set)),
            encoder=LazyEncoder, safe=False
        )

    return _view


def dict_choice(choice):
    return {'value': choice[0], 'label': choice[1]}


relationships: ViewType = view_maker(choices_data.relationships, serializers.choices.CharChoices)
underage_relationships: ViewType = view_maker(choices_data.underage_relationships, serializers.choices.CharChoices)
transportation_modes: ViewType = view_maker(choices_data.transportation_modes, serializers.choices.CharChoices)
genders: ViewType = view_maker(choices_data.genders, serializers.choices.CharChoices)
travel_documents: ViewType = view_maker(choices_data.travel_documents, serializers.choices.CharChoices)
residence_choices: ViewType = view_maker(choices_data.residence_choices, serializers.choices.CharChoices)
transportation_means: ViewType = view_maker(choices_data.transportation_means, serializers.choices.CharChoices)
