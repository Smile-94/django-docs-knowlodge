from _library.filters import GenericSearchFilter
from apps.order.models.order_model import Order


# <<--------------------------------- Order Filter --------------------------------->>
class OrderFilter(GenericSearchFilter):
    class Meta(GenericSearchFilter.Meta):
        model = Order
