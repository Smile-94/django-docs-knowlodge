import re

from django.db.models import Q
from rest_framework import serializers

from apps.user.models.user_model import User


# <<------------------------------------Registration Serializer---------------------------------------->>
class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=30, required=True)
    confirm_password = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(required=True)
    phone = serializers.CharField(max_length=20, required=True)

    def validate_phone(self, value):
        pattern = r"^\+[1-9]\d{1,14}$"
        if not re.match(pattern, value):
            raise serializers.ValidationError("Phone number must be in international format (e.g., +1234567890).")
        return value

    def validate_password(self, value):
        """
        Validate password complexity:
        - Length already enforced by min_length/max_length.
        - At least one uppercase letter.
        - At least one lowercase letter.
        - At least one digit.
        - At least one special character.
        """
        errors = []

        if not any(char.isupper() for char in value):
            errors.append("Password must contain at least one uppercase letter.")

        if not any(char.islower() for char in value):
            errors.append("Password must contain at least one lowercase letter.")

        if not any(char.isdigit() for char in value):
            errors.append("Password must contain at least one digit.")

        special_chars = "!@#$%^&*()_+-=[]{}|;:'\",.<>/?`~"
        if not any(char in special_chars for char in value):
            errors.append("Password must contain at least one special character.")

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def validate(self, data):
        errors = {}

        # Password match validation
        if data["password"] != data["confirm_password"]:
            errors["confirm_password"] = "Passwords do not match."

        # Single DB query for uniqueness
        existing_users = User.objects.only("username", "email", "phone").filter(
            Q(username=data["username"]) | Q(email=data["email"]) | Q(phone=data["phone"])
        )

        # Map existing conflicts
        for user in existing_users:
            if user.username == data["username"]:
                errors["username"] = "A user with this username already exists."
            if user.email == data["email"]:
                errors["email"] = "A user with this email already exists."
            if user.phone == data["phone"]:
                errors["phone"] = "A user with this phone number already exists."

        # Raise all errors at once
        if errors:
            raise serializers.ValidationError(errors)

        return data
