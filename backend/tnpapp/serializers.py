from django.core.exceptions import ValidationError
from rest_framework import serializers
from typing import Any
from tnpapp.models import CustomUser
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators


class BaseUserModelSerializer(serializers.ModelSerializer):
    # TODO : check for better options
    __password_help_html_str = """<ul>
        <li>Your password must contain at least 8 characters.</li>
        <li>Your password can’t be a commonly used password.</li>
        <li>Your password can’t be entirely numeric.</li>
    </ul>"""

    password1 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Password"},
        help_text=__password_help_html_str,
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password", "placeholder": "Confirm Password"},
    )

    class Meta:
        model: Any
        exclude = (
            "user_permissions",
            "groups",
            "password",
        )
        read_only_fields = (
            "is_active",
            "is_staff",
            "is_superuser",
            "last_login",
            "date_joined",
            "role",
        )

    def validate(self, attrs: Any) -> Any:
        # TODO : simplify the checks
        pass1 = attrs.get("password1")
        pass2 = attrs.get("password2")
        if self.partial:
            if pass1 is None and pass2 is None:
                return attrs
        if pass1 is None:
            raise serializers.ValidationError({"password1": "password is None"})
        if pass2 is None:
            raise serializers.ValidationError({"password2": "confirm password is None"})
        try:
            validators.validate_password(pass1)
        except ValidationError as exc:
            raise serializers.ValidationError({"password1": exc.messages})
        if pass1 != pass2:
            raise serializers.ValidationError({"password2": "passwords do not match"})
        attrs["password"] = make_password(pass1)

        # cleanup
        attrs.pop("password1")
        attrs.pop("password2")
        return attrs


class CustomUserSerializer(BaseUserModelSerializer):
    class Meta(BaseUserModelSerializer.Meta):
        model = CustomUser
