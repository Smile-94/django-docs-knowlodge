from django.db import models


# <<------------------------------------Signal Choices---------------------------------------->>
class SignalStatusChoices(models.TextChoices):
    PENDING = "pending", "Pending"
    PROCESSING = "processing", "Processing"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"
