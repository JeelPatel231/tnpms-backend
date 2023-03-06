from rest_framework import serializers
from typing import Any


class BaseUserModelSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Confirm Password"},
    )

    class Meta:
        model: Any
        exclude = (
            "is_staff",
            "is_superuser",
            "is_active",
            "user_permissions",
            "groups",
            "password",
            "last_login",
            "date_joined",
        )

    def validate(self, attrs: Any) -> Any:
        attrs["password"] = attrs["password1"]
        if attrs.pop("password1") != attrs.pop("password2"):
            raise serializers.ValidationError({"password": "passwords do not match"})
        return attrs

    def save(self):
        return self.Meta.model.objects.create_user(**self.validated_data)