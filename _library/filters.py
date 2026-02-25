import datetime

from django.core.exceptions import FieldError
from django.db.models import Q
from django.utils import timezone
import django_filters


def build_and_filter(query_filter: dict, query_params):
    q_objects = Q()
    for field_lookup, param_name in query_filter.items():
        value = query_params.get(param_name)
        if value not in [None, ""]:
            if isinstance(value, str) and value.lower() == "true":
                value = True
            elif isinstance(value, str) and value.lower() == "false":
                value = False

            q_objects &= Q(**{field_lookup: value})

    return q_objects


def build_or_filter(query_filter: dict, query_params):
    q_objects = Q()
    for field_lookup, param_name in query_filter.items():
        value = query_params.get(param_name)
        if value not in [None, ""]:
            if isinstance(value, str) and value.lower() == "true":
                value = True
            elif isinstance(value, str) and value.lower() == "false":
                value = False

            q_objects |= Q(**{field_lookup: value})

    return q_objects


class GenericSearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="_get_search_result", label="Search")
    from_date = django_filters.DateFilter(method="filter_from_date", label="From Date")
    to_date = django_filters.DateFilter(method="filter_to_date", label="To Date")

    class Meta:
        model = None
        fields = ["search", "from_date", "to_date"]

    def __init__(self, *args, **kwargs):
        self.search_fields = kwargs.pop("search_fields", ["id"])
        super().__init__(*args, **kwargs)

        # Validate search fields against model
        model_fields = [f.name for f in self._meta.model._meta.get_fields()]
        for field in self.search_fields:
            base_field = field.split("__")[0]
            if base_field not in model_fields:
                raise FieldError(f"Invalid search field '{field}' for model {self._meta.model.__name__}")

    def _get_search_result(self, queryset, name, value):
        if not value:
            return queryset

        q_objects = Q()

        for field in self.search_fields:
            # Extract the base field name (before "__")
            base_field = field.split("__")[0]

            # Skip numeric filters if value is not numeric
            if (base_field.endswith("id") or base_field == "id") and not value.isnumeric():
                continue

            q_objects |= Q(**{field: value})

        return queryset.filter(q_objects)

    def filter_from_date(self, queryset, name, value):
        """Always filters by created_at >= from_date"""
        if value:
            dt = timezone.make_aware(datetime.datetime.combine(value, datetime.time.min))
            return queryset.filter(created_at__gte=dt)
        return queryset

    def filter_to_date(self, queryset, name, value):
        """Always filters by created_at <= to_date"""
        if value:
            dt = timezone.make_aware(datetime.datetime.combine(value, datetime.time.max))
            return queryset.filter(created_at__lte=dt)
        return queryset
