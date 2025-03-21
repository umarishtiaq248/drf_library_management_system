from rest_framework import serializers
from django.contrib.auth import authenticate
from auth_app.models import CustomUser
from rest_framework.authtoken.models import Token


class AuthenticationSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = authenticate(
            request=self.context.get("request"), username=username, password=password
        )
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        data["user"] = user
        return data


class CRUDSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return {"username": user.username, "token": token.key}

    def update(self, instance, validated_data):
        password = validated_data.pop("password")
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    class Meta:
        model = CustomUser
        fields = ["username", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }
