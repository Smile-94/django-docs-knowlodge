import datetime

from django.db.models import Model


def generate_custom_id(id_prefix: str, field: str, model_class: type[Model]) -> str:
    """
    Generates a unique custom ID with prefix, date, and incremented counter (safe under concurrency).
    """
    if not hasattr(model_class, field):
        raise ValueError(f"The field '{field}' does not exist in the model '{model_class.__name__}'.")

    current_date = datetime.date.today()
    formatted_date = current_date.strftime("%d%m%y")
    base_prefix = f"{id_prefix}{formatted_date}"

    # Lock rows that start with the prefix + date
    latest_instance = (
        model_class.objects.filter(**{f"{field}__startswith": base_prefix})
        .select_for_update(skip_locked=True)
        .order_by(f"-{field}")
        .first()
    )

    if latest_instance:
        latest_field_value = getattr(latest_instance, field, "")
        try:
            previous_counter = int(latest_field_value[-4:])
            new_counter = (previous_counter + 1) % 10000
        except ValueError:
            new_counter = 1
    else:
        new_counter = 1

    formatted_counter = str(new_counter).zfill(4)
    return f"{base_prefix}{formatted_counter}"
