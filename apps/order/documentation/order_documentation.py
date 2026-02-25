from drf_spectacular.utils import OpenApiExample, OpenApiParameter, OpenApiResponse, extend_schema

from _library.dataclass import ErrorResponse, SuccessResponse

TAG_NAME = "Order"


# <<--------------------------------- Order List Documentation --------------------------------->>
class OrderDocumentation:
    @staticmethod
    def list():
        return extend_schema(
            tags=[TAG_NAME],
            summary="List Orders",
            description=(
                "Retrieve a paginated list of orders with filtering, searching and "
                "dynamic field selection support.\n\n"
                "**Query Features:**\n"
                "- Filter using whitelisted query parameters\n"
                "- Search using indexed safe fields\n"
                "- Dynamic field selection via `field_list`\n"
                "- Supports pagination\n\n"
                "**Supported Query Params:**\n"
                "- active_status\n"
                "- status\n"
                "- action\n"
                "- instrument\n"
                "- field_list (comma separated)\n"
                "- search params (id, order_id, account_id)\n\n"
                "**Security:**\n"
                "- Requires authentication\n"
                "- Only accessible to authorized device users\n"
            ),
            request=None,  # GET → No body
            parameters=[
                OpenApiParameter(
                    name="limit",
                    type=int,
                    description="Number of items to return per page (for pagination).",
                    required=False,
                ),
                OpenApiParameter(
                    name="offset",
                    type=int,
                    description="Offset index for pagination (starting point).",
                    required=False,
                ),
                OpenApiParameter(
                    name="from_date",
                    type=str,
                    description="Filter services by created_at >= from_date.",
                    required=False,
                ),
                OpenApiParameter(
                    name="to_date",
                    type=str,
                    description="Filter services by created_at <= to_date.",
                    required=False,
                ),
                OpenApiParameter(
                    name="active_status",
                    type=str,
                    description="Filter services by active_status.",
                    required=False,
                ),
                OpenApiParameter(
                    name="status",
                    type=str,
                    description="Filter services by status.",
                    required=False,
                ),
                OpenApiParameter(
                    name="action",
                    type=str,
                    description="Filter services by action.",
                    required=False,
                ),
                OpenApiParameter(
                    name="instrument",
                    type=str,
                    description="Filter services by instrument.",
                    required=False,
                ),
                OpenApiParameter(
                    name="field_list",
                    type=str,
                    description="Comma separated list of fields to include in response.",
                    required=False,
                ),
                OpenApiParameter(
                    name="search",
                    type=str,
                    description="Search term for filtering services by name or ID.",
                    required=False,
                ),
            ],
            responses={
                # ================= SUCCESS =================
                200: OpenApiResponse(
                    response=SuccessResponse,
                    description="Orders retrieved successfully",
                    examples=[
                        OpenApiExample(
                            name="Successful Order List",
                            value={
                                "status": 200,
                                "message": "Retrieved Category List",
                                "data": {
                                    "count": 2,
                                    "next": None,
                                    "previous": None,
                                    "results": [
                                        {
                                            "id": 1,
                                            "order_id": "ORD-1001",
                                            "action": "BUY",
                                            "instrument": "EURUSD",
                                            "entry_price": 1.085,
                                            "stop_loss": 1.080,
                                            "take_profit": 1.090,
                                            "status": "OPEN",
                                        }
                                    ],
                                },
                                "links": None,
                            },
                            response_only=True,
                        )
                    ],
                ),
                # ================= CLIENT ERROR =================
                400: OpenApiResponse(
                    response=ErrorResponse,
                    description="Invalid query parameters or field_list validation error",
                    examples=[
                        OpenApiExample(
                            name="Invalid Query Param",
                            value={
                                "status": 400,
                                "message": "Invalid query params",
                                "invalid_params": ["wrong_param"],
                                "supported_params": ["active_status", "status", "action", "instrument"],
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Invalid Field List",
                            value={
                                "status": 400,
                                "message": "Invalid field_list in field_list parameter",
                                "invalid_fields": ["wrong_field"],
                                "supported_fields": "id, order_id, action, instrument",
                            },
                            response_only=True,
                        ),
                    ],
                ),
                # ================= AUTH ERROR =================
                401: OpenApiResponse(
                    response=ErrorResponse,
                    description="Authentication required",
                    examples=[
                        OpenApiExample(
                            name="Unauthorized",
                            value={
                                "status": 401,
                                "message": "Authentication credentials were not provided.",
                            },
                            response_only=True,
                        )
                    ],
                ),
                # ================= SERVER ERROR =================
                500: OpenApiResponse(
                    response=ErrorResponse,
                    description="Internal server error",
                    examples=[
                        OpenApiExample(
                            name="Server Error",
                            value={
                                "status": 500,
                                "message": "Internal Server Error",
                            },
                            response_only=True,
                        )
                    ],
                ),
            },
        )

    @staticmethod
    def detail():
        return extend_schema(
            tags=[TAG_NAME],
            summary="Retrieve Order Details",
            description=(
                "Retrieve a single order by primary key.\n\n"
                "**Features:**\n"
                "- Fetch order by `pk`\n"
                "- Supports dynamic `field_list` selection\n"
                "- Supports safe filtering via query params\n"
                "- Returns only orders belonging to authenticated user\n"
                "- Prefetches related `history` data\n\n"
                "**Query Parameters:**\n"
                "- field_list (comma separated fields)\n"
                "- Supported filter params (validated dynamically)\n\n"
                "**Security:**\n"
                "- Authentication required\n"
                "- Users can only access their own orders\n"
            ),
            parameters=[
                OpenApiParameter(
                    name="field_list",
                    type=str,
                    location=OpenApiParameter.QUERY,
                    description="Comma separated fields for dynamic field selection",
                    required=False,
                ),
            ],
            request=None,
            responses={
                # ================= SUCCESS =================
                200: OpenApiResponse(
                    response=SuccessResponse,
                    description="Order retrieved successfully",
                    examples=[
                        OpenApiExample(
                            name="Order Detail Success",
                            value={
                                "status": 200,
                                "message": "Retrieved Permission",
                                "data": {
                                    "id": 10,
                                    "order_id": "ORD-1001",
                                    "action": "BUY",
                                    "instrument": "EURUSD",
                                    "entry_price": 1.085,
                                    "stop_loss": 1.080,
                                    "take_profit": 1.090,
                                    "status": "OPEN",
                                },
                                "links": None,
                            },
                            response_only=True,
                        )
                    ],
                ),
                # ================= CLIENT ERROR =================
                400: OpenApiResponse(
                    response=ErrorResponse,
                    description="Validation error or order not found",
                    examples=[
                        OpenApiExample(
                            name="Invalid Query Param",
                            value={
                                "status": 400,
                                "message": "Invalid query params",
                                "invalid_params": ["wrong_param"],
                                "supported_params": ["status", "action", "instrument"],
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Invalid Field List",
                            value={
                                "status": 400,
                                "message": "Invalid field_list in field_list parameter",
                                "invalid_fields": ["wrong_field"],
                                "supported_fields": "id, order_id, action, instrument",
                            },
                            response_only=True,
                        ),
                        OpenApiExample(
                            name="Order Not Found",
                            value={
                                "status": 400,
                                "message": "Permission not found with the id 10",
                                "id": 10,
                            },
                            response_only=True,
                        ),
                    ],
                ),
                # ================= AUTH ERROR =================
                401: OpenApiResponse(
                    response=ErrorResponse,
                    description="Authentication required",
                    examples=[
                        OpenApiExample(
                            name="Unauthorized",
                            value={
                                "status": 401,
                                "message": "Authentication credentials were not provided.",
                            },
                            response_only=True,
                        )
                    ],
                ),
                # ================= SERVER ERROR =================
                500: OpenApiResponse(
                    response=ErrorResponse,
                    description="Internal server error",
                    examples=[
                        OpenApiExample(
                            name="Server Error",
                            value={
                                "status": 500,
                                "message": "Internal Server Error",
                            },
                            response_only=True,
                        )
                    ],
                ),
            },
        )
