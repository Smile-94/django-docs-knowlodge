from rest_framework import serializers


# <<--------------------------------- Signals Parse Serializer --------------------------------->>
class SignalsParseSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
