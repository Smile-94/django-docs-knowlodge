from rest_framework import serializers

from apps.common.generic_mixin.serializer_mixing import FilterFieldMixin


# <<--------------------------------- Order Serializer --------------------------------->>
class OrderListSerializer(FilterFieldMixin, serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_id = serializers.CharField(read_only=True)
    action = serializers.CharField(read_only=True)
    instrument = serializers.CharField(read_only=True)
    entry_price = serializers.DecimalField(max_digits=19, decimal_places=4, read_only=True)
    stop_loss = serializers.DecimalField(max_digits=19, decimal_places=4, read_only=True)
    take_profit = serializers.DecimalField(max_digits=19, decimal_places=4, read_only=True)
    status = serializers.CharField(read_only=True)
    active_status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


# <<--------------------------------- Order History Serializer --------------------------------->>
class OrderHistorySerializer(FilterFieldMixin, serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


# <<--------------------------------- Order Serializer --------------------------------->>
class OrderSerializer(FilterFieldMixin, serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_id = serializers.CharField(read_only=True)
    action = serializers.CharField(read_only=True)
    instrument = serializers.CharField(read_only=True)
    entry_price = serializers.DecimalField(max_digits=19, decimal_places=4, read_only=True)
    stop_loss = serializers.DecimalField(max_digits=19, decimal_places=4, read_only=True)
    take_profit = serializers.DecimalField(max_digits=19, decimal_places=4, read_only=True)
    status = serializers.CharField(read_only=True)
    active_status = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    order_history = serializers.ListSerializer(source="history", child=OrderHistorySerializer(), read_only=True)
