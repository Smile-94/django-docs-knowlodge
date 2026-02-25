from rest_framework import serializers


class FilterFieldMixin:
    """
    Wrapper mixin to filter serializer fields using `field_list`.

    field_list:
        - "*" → all fields
        - "id,name,children"
        - ["id", "name"]
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        field_list = self.context.get("field_list")

        # No filtering or wildcard
        if not field_list or field_list == "*":
            return

        # Normalize input
        if isinstance(field_list, (list, tuple, set)):
            requested_fields = {f.strip() for f in field_list}
        elif isinstance(field_list, str):
            requested_fields = {f.strip() for f in field_list.split(",")}
        else:
            raise serializers.ValidationError({"field_list": "Must be '*' or list or comma-separated string"})

        allowed_fields = self._get_allowed_fields()

        # Reject invalid fields
        invalid = requested_fields - allowed_fields
        if invalid:
            raise serializers.ValidationError({"field_list": f"Invalid fields: {', '.join(invalid)}"})

        #  Filter fields
        for field_name in list(self.fields.keys()):
            if field_name not in requested_fields:
                self.fields.pop(field_name)

    def _get_allowed_fields(self) -> set[str]:
        """
        Allowed = serializer fields + model fields (if ModelSerializer)
        """
        serializer_fields = set(self.fields.keys())
        model_fields = set()

        meta = getattr(self, "Meta", None)
        model = getattr(meta, "model", None)

        if model:
            model_fields = {f.name for f in model._meta.get_fields()}

        return serializer_fields | model_fields
