from django.core.serializers import serialize
from rest_framework import serializers


class AddItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=1)
    product_id = serializers.IntegerField()

