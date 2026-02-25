from django.db import models


# <<------------------------------------Order Choices---------------------------------------->>
class Action(models.TextChoices):
    BUY = "BUY", "Buy"
    SELL = "SELL", "Sell"


# <<------------------------------------Order Choices---------------------------------------->>
class OrderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    EXECUTED = "executed", "Executed"
    CLOSED = "closed", "Closed"
    REJECTED = "rejected", "Rejected"
    CANCELLED = "cancelled", "Cancelled"
