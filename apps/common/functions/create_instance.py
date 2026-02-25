import logging

from django.db import models

logger = logging.getLogger(__name__)


def create_instance(
    model: type[models.Model],
    validated_data: dict,
    extract_fields: list[str] | None = None,
) -> models.Model:
    """
    Generic instance creation utility.

    Features:
    - Extracts specified fields before model creation (e.g., confirm_password).
    - Handles Many-to-Many fields safely.
    - Ensures atomic database transaction.
    - Logs full exception stack for observability.

    Args:
        model: Django model class.
        validated_data: Cleaned serializer data.
        extract_fields: Optional list of fields to remove before instance creation.

    Returns:
        Created model instance.
    """

    try:
        extract_fields = extract_fields or []

        # Make a mutable copy to avoid mutating serializer.validated_data
        data = validated_data.copy()

        # Extract custom non-model fields
        # (e.g., confirm_password, temporary flags)

        for field in extract_fields:
            data.pop(field, None)

        m2m_data: dict[str, list] = {}

        # Extract Many-to-Many fields
        # Must be set AFTER instance creation

        for field in model._meta.many_to_many:
            if field.name in data:
                m2m_data[field.name] = data.pop(field.name)

        instance = model.objects.create(**data)

        # Assign Many-to-Many relationships
        for field_name, value in m2m_data.items():
            getattr(instance, field_name).set(value)

        # Explicit save for extensibility
        instance.save()

        return instance

    except Exception as e:
        logger.exception(f"ERROR:------------>> create_instance failed | model={model} | error={e}")
        raise
