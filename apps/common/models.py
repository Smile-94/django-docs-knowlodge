from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


# <<------------------------------------Active Status Choices---------------------------------------->>
class ActiveStatusChoices(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"


# <<------------------------------------Timestamped Model---------------------------------------->>
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# <<------------------------------------User Stamp Model---------------------------------------->>
class UserStampModel(models.Model):
    """
    related_name work by this pattern:
    %(class)s :: is the model class name in lowercase.
    model_name_created_by
    model_name_updated_by

    example::
    prescriptiondrugs_created_by
    prescriptiondrugs_updated_by
    """

    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="%(class)s_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="%(class)s_updated_by")

    class Meta:
        abstract = True


# <<------------------------------------Base Model---------------------------------------->>
class BaseModel(models.Model):
    """
    Base Model for all models
    """

    active_status = models.CharField(max_length=10, choices=ActiveStatusChoices.choices, default=ActiveStatusChoices.ACTIVE.value)
    description = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True
