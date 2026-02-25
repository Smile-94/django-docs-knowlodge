from rest_framework import serializers

from apps.broker.models.broker_account_model import BrokerAccount


# <<--------------------------------- Broker Account Serializer --------------------------------->>
class BrokerAccountSerializer(serializers.Serializer):
    account_name = serializers.CharField(max_length=100, required=True)
    account_id = serializers.CharField(max_length=100, required=True)
    api_key = serializers.CharField(max_length=255, required=True)

    def validate(self, value):
        # Single DB query for uniqueness
        existing_users = BrokerAccount.objects.only("account_id").filter(account_id=value["account_id"]).first()

        if existing_users:
            raise serializers.ValidationError("Broker account already exists.")
        return value
