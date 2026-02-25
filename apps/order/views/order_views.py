import logging

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from _library.error_codes import BAD_REQUEST_DEVELOPER_ERROR, INTERNAL_SERVER_ERROR
from _library.filters import build_and_filter
from _library.functions.allowed_method import allowed_methods
from _library.functions.formatters import response_formatter
from _library.functions.paginator import get_paginate_and_serialized_data
from _library.functions.parse_field_list import get_field_list_from_request, get_supported_field_list_string
from _library.success_code import SUCCESS_RESPONSE_200
from apps.common.authentication import DeviceTokenAuthentication
from apps.common.functions.validators import validate_field_list, validate_query_params
from apps.order.documentation.order_documentation import OrderDocumentation
from apps.order.filters.order_filter import OrderFilter
from apps.order.models.order_model import Order
from apps.order.serializers.order_serializer import OrderListSerializer, OrderSerializer

logger = logging.getLogger(__name__)

# <<--------------------------------- Order List View --------------------------------->>


@allowed_methods("GET")
class OrderListAPIView(APIView):
    authentication_classes = [DeviceTokenAuthentication]
    permission_classes = [IsAuthenticated]

    model_class = Order
    serializer_class = OrderListSerializer
    filter_class = OrderFilter
    # Search is restricted to indexed / safe fields only
    search_fields = ["id__exact", "order_id__exact", "signal__account__account_id__istartswith"]
    # Whitelisted query params → ORM lookups
    query_filter = {"active_status": "active_status", "status": "status", "action": "action", "instrument": "instrument__exact"}

    def __init__(self, *args, **kwargs):
        # Default response fields (can be overridden via field_list param)
        self.field_list = ["id", "order_id", "action", "instrument", "entry_price", "stop_loss", "take_profit", "status"]
        # Assigned dynamically after filtering
        self.queryset = None
        super().__init__(*args, **kwargs)

    @OrderDocumentation.list()
    def get(self, request):
        try:
            # Step 1: Validate query parameters against allowed filters
            valid_params, invalid_params = validate_query_params(request, self.query_filter, query_type="list")
            if invalid_params:
                data = {"message": "Invalid query params", "invalid_params": invalid_params, "supported_params": valid_params}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            # Step 2: Extract and validate dynamic field selection
            if request.query_params.get("field_list"):
                self.field_list = get_field_list_from_request(request)

            invalid_fields = validate_field_list(
                field_list=self.field_list, serializer_class=self.serializer_class, model_class=self.model_class
            )
            if invalid_fields:
                data = {
                    "message": "Invalid field_list in field_list parameter",
                    "invalid_fields": invalid_fields,
                    "supported_fields": get_supported_field_list_string(self.serializer_class),
                }
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            # Step 3: Build base queryset using safe AND-based filters
            filtered_query = self.model_class.objects.filter(build_and_filter(self.query_filter, request.query_params)).filter(
                user=request.user
            )

            # Apply search + additional filter logic
            self.queryset = self.filter_class(request.GET, queryset=filtered_query, search_fields=self.search_fields).qs

            # Step 4: Paginate and serialize with dynamic fields
            data = get_paginate_and_serialized_data(self.serializer_class, self.queryset, request, field_list=self.field_list)

            # data = {"message": "Retrieved Category List", "results": data}
            data["message"] = "Retrieved Category List"
            return response_formatter(SUCCESS_RESPONSE_200, data)

        except Exception as e:
            logger.exception(f"ERROR:---------->>Order List View error: {e}")
            return response_formatter(INTERNAL_SERVER_ERROR)


# <<--------------------------------- Order Detail View --------------------------------->>
@allowed_methods("GET")
class OrderDetailAPIView(APIView):
    authentication_classes = [DeviceTokenAuthentication]
    permission_classes = [IsAuthenticated]

    model_class = Order
    serializer_class = OrderSerializer
    filter_class = OrderFilter

    def __init__(self, *args, **kwargs):
        # Default response fields (can be overridden via field_list param)
        self.field_list = ["id", "order_id", "action", "instrument", "entry_price", "stop_loss", "take_profit", "status"]
        # Assigned dynamically after filtering
        self.queryset = None
        super().__init__(*args, **kwargs)

    @OrderDocumentation.detail()
    def get(self, request, pk):
        try:
            # Step 1: Validate query parameters against allowed filters
            valid_params, invalid_params = validate_query_params(request, query_type="retrieve")
            if invalid_params:
                data = {"message": "Invalid query params", "invalid_params": invalid_params, "supported_params": valid_params}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            # Step 2: Extract and validate dynamic field selection
            if request.query_params.get("field_list"):
                self.field_list = get_field_list_from_request(request)

            # 3. Ensure requested fields exist in serializer/model
            invalid_fields = validate_field_list(
                field_list=self.field_list, serializer_class=self.serializer_class, model_class=self.model_class
            )
            if invalid_fields:
                data = {
                    "message": "Invalid field_list in field_list parameter",
                    "invalid_fields": invalid_fields,
                    "supported_fields": get_supported_field_list_string(self.serializer_class),
                }
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            # 4. Fetch permission safely by primary key
            self.queryset = self.model_class.objects.filter(pk=pk, user=request.user).prefetch_related("history").first()
            if not self.queryset:
                data = {"message": f"Permission not found with the id {pk}", "id": pk}
                return response_formatter(BAD_REQUEST_DEVELOPER_ERROR, data)

            # 5. Serialize only requested fields
            data = self.serializer_class(self.queryset, context={"field_list": self.field_list}).data
            data["message"] = "Retrieved Permission"

            return response_formatter(SUCCESS_RESPONSE_200, data)

        except Exception as e:
            logger.exception(f"ERROR:-------------->> (PermissionDetailView) error: {e}")
            return response_formatter(INTERNAL_SERVER_ERROR)
