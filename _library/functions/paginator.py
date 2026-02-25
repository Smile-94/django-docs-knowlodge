from rest_framework.pagination import LimitOffsetPagination


class LimitOffsetOrAllPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.count = self.get_count(queryset)
        self.limit = self.get_limit(request)
        self.offset = self.get_offset(request)

        if self.limit is None:
            self.limit = self.count
            self.display_page_controls = False
            return list(queryset)

        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset : self.offset + self.limit])

    def get_paginated_response(self, data):
        return {
            "count": self.count,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        }

    def make_pagination(self, queryset, request, view=None):
        data = self.paginate_queryset(queryset, request, view)
        return self.get_paginated_response(data)


def get_paginate_serialized_data(serializer_class, paginated_queryset, field_list="*"):
    paginated_queryset["results"] = serializer_class(
        paginated_queryset.get("results"), many=True, context={"field_list": field_list}
    ).data
    return paginated_queryset


def get_paginate_and_serialized_data(serializer_class, queryset, request, field_list="*", view=None):
    """
    This is function combine 2 functionalities both pagination and serialization.
    This function will return a paginated queryset with serialized data for the view.
    Use the limit-offset pagination for the queryset.
    return:: serialized_data

    example return data:: {
            "count": 1,
            "next": /next_link_url,
            "previous": /previous_link_url,
            "results": {"hello": "world"}, // it is serialized queryset data
        }
    """

    paginated_queryset = LimitOffsetOrAllPagination().make_pagination(queryset, request, view)
    return get_paginate_serialized_data(serializer_class, paginated_queryset, field_list)
