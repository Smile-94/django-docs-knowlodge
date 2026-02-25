from rest_framework import serializers


# <<------------------------------------Login Serializer---------------------------------------->>
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)

    def validate_username(self, value):
        if not value.isalnum():
            raise serializers.ValidationError("Username must be alphanumeric.")
        return value


# <<------------------------------------Refresh Token Serializer---------------------------------------->>
class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=255, required=True)
