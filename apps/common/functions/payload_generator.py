from rest_framework import serializers


def get_payload_data(serializer_class) -> dict:
    """
    Generate a sample payload description from a DRF serializer.

    Supports:
    - Serializer
    - ModelSerializer
    - Nested serializers
    - ListSerializer

    Returns:
        dict: Field-wise payload hints
    """
    serializer = serializer_class()
    payload = {}

    for field_name, field in serializer.get_fields().items():
        payload[field_name] = _describe_field(field)

    return payload


def _describe_field(field):
    """
    Describe a single serializer field.
    """
    # Nested serializer
    if isinstance(field, serializers.ListSerializer):
        return [_describe_field(field.child)]

    if isinstance(field, serializers.Serializer):
        return {name: _describe_field(child) for name, child in field.get_fields().items()}

    field_type = field.__class__.__name__.replace("Field", "").lower()

    description_parts = [field_type]

    if field.required:
        description_parts.append("This field is required")
    else:
        description_parts.append("Optional")

    if getattr(field, "allow_null", False):
        description_parts.append("Nullable")

    if getattr(field, "allow_blank", False):
        description_parts.append("Can be blank")

    return ", ".join(description_parts)
