from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    first_name       = serializers.CharField(allow_null=False, write_only=True)
    last_name        = serializers.CharField(allow_null=False, write_only=True)
    # confirm_password = serializers.CharField(allow_null=False, write_only=False)

    class Meta:
        model = get_user_model()
        fields = ("phone_number", "first_name", "last_name", "password")

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
