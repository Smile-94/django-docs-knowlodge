def get_field_list_from_request(request):
    """
    Extract and normalize `field_list` from request query params.

    Supported:
    - ?field_list=*              → "*"
    - ?field_list=id,name,slug   → ["id", "name", "slug"]
    - missing / empty            → "*"

    Returns:
        list[str] | str
    """
    field_list_param = request.query_params.get("field_list")

    if not field_list_param:
        return "*"

    field_list_param = field_list_param.strip()

    if field_list_param == "*":
        return "*"

    return [field.strip() for field in field_list_param.split(",") if field.strip()]


def get_supported_field_list_string(serializer_class) -> str:
    """
    Return a comma-separated string of supported fields
    from a DRF Serializer or ModelSerializer.

    Example:
        "id,name,slug,created_at"
    """
    if not serializer_class:
        return ""

    serializer = serializer_class()
    fields = serializer.get_fields().keys()

    return ",".join(fields)
