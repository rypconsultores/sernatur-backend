import re
from typing import Pattern, Optional

from django.db.models import Q, QuerySet
from django.http import QueryDict
from rest_framework.exceptions import APIException


class FilterableViewSetMixin(object):
    special_fields = (
        #('contract_type', 'contract_type__id_contract_type')
    )

    def get_queryset(self) -> QuerySet:
        queryset: QuerySet = self.queryset
        query_string: QueryDict = self.request.query_params

        try:
            if 'order_by' in query_string:
                queryset = queryset.order_by(*query_string['order_by'].split(','))
        except Exception as exc:
            raise APIException(f"Cannot order fields: {str(exc)}")

        filter: str
        value: str

        re_filters: Pattern = re.compile(
            r'([\w_-]+)\.(is|in|gt|lt|gte|lte|startswith|endswith|like|i?contains)'
        )

        q_query: Optional[Q] = None
        q_operator: str = 'and'

        for filter, value in query_string.items():
            if filter.endswith('[]'):
                value = query_string.getlist(filter)
                filter = filter[0:-2]

            if filter == 'or':
                q_operator: str = 'or'
                continue

            field: str = re.sub(re_filters,  r'\1', filter)

            for special_field in self.special_fields:
                if field == special_field[0]:
                    filter = re.sub(
                        re_filters, special_field[1] + r'\2', filter
                    )

            if re.search(re_filters, filter):
                if value == '\x00':
                    value = None

                if filter.endswith('.is'):
                    filter = '.'.join(filter.split('.')[0:-1])
                else:
                    filter = re.sub(re_filters, r'\1__\2', filter)

                q_filter = Q(**{filter: value})

                if q_query is None:
                    q_query = q_filter
                elif q_operator == 'or':
                    q_query |= q_filter
                    q_operator = 'and'
                else:
                    q_query &= q_filter

        if q_query is not None:
            try:
                queryset = queryset.filter(q_query)
            except Exception as exc:
                raise APIException(f"Cannot filter: {str(exc)}")

        return queryset
