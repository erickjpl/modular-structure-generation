from rest_framework.serializers import (
  BooleanField,
  CharField,
  DateTimeField,
  EmailField,
  IntegerField,
  Serializer,
  UUIDField,
)


class OrderResponseSerializer(Serializer):
  id = UUIDField(read_only=True)
  username = CharField(read_only=True)
  email = EmailField(read_only=True)
  first_name = CharField(read_only=True)
  last_name = CharField(read_only=True)
  age = IntegerField(read_only=True)
  is_active = BooleanField(read_only=True)
  created_at = DateTimeField(read_only=True)
  updated_at = DateTimeField(read_only=True)
  deleted_at = DateTimeField(read_only=True)
