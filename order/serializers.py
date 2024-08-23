from rest_framework import serializers
from .models import Order ,OrderItem

class OrderItemSerializer (serializers.Serializer):
    class Meta:
        model= OrderItem
        fields="__all__"

class OrderSerializer (serializers.ModelSerializer):
    class Meta:
        model= Order
        fields="__all__"