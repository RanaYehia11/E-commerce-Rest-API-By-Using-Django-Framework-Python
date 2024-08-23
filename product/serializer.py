from rest_framework import serializers
from .models import Product,Review

class Product_serializer(serializers.ModelSerializer):
    reviews=serializers.SerializerMethodField(method_name='get_reviews',read_only=True)
    class Meta:
        model=Product
        fields= "__all__"
  

    def get_reviews(self,obj):
        reviews=obj.reviews.all()
        serializer=Review_serializer(reviews,many=True)
        return serializer.data

class Review_serializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields= "__all__"