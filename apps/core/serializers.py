from rest_framework import serializers

from apps.core.models import DicoTable, Event, TablePrice, TypeTicket, User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "phone_number", "password",
            "type_user", "fcm_token", "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, required=False)

    class Meta:
        model = User
        fields = ["phone_number", "fcm_token", "is_active", "username", "email", "password"]

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id", "name", "description", "flyer_url",
            "start_time", "end_time", "event_state",
            "created_by", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "name", "start_time", "end_time", "event_state"]


class DicoTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DicoTable
        fields = ["id", "number", "table_type", "capacity", "table_state"]
        read_only_fields = ["id"]


class TypeTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTicket
        fields = ["id", "name", "event", "available_quantity", "max_override", "price"]
        read_only_fields = ["id"]


class TablePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TablePrice
        fields = ["id", "table", "event", "price"]
        read_only_fields = ["id"]
