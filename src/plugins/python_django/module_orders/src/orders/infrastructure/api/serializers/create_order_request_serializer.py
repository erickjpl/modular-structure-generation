from rest_framework.serializers import BooleanField, CharField, EmailField, IntegerField, Serializer


class CreateOrderRequestSerializer(Serializer):
  username = CharField(max_length=20)
  email = EmailField()
  password = CharField(min_length=8)
  first_name = CharField(max_length=100)
  last_name = CharField(max_length=100)
  age = IntegerField(min_value=0, max_value=150)
  is_active = BooleanField(required=False, default=True)
