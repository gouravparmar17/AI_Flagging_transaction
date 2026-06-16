from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    full_name = serializers.CharField(write_only=True)
    company_name = serializers.CharField(required=False, allow_blank=True, write_only=True)
    phone = serializers.CharField(required=False, allow_blank=True, write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password", "full_name", "company_name", "phone"]

    def create(self, validated_data):
        if not validated_data.get("username"):
            base_username = validated_data["email"].split("@")[0]
            username = base_username
            idx = 1
            while User.objects.filter(username=username).exists():
                idx += 1
                username = f"{base_username}{idx}"
            validated_data["username"] = username
        full_name = validated_data.pop("full_name")
        company_name = validated_data.pop("company_name", "")
        phone = validated_data.pop("phone", "")
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, full_name=full_name, company_name=company_name, phone=phone)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["full_name", "company_name", "phone"]


class MeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "created_at", "updated_at", "profile"]


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)
