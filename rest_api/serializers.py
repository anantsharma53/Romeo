from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"
    def create(self,validated_data):
        user=User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number']
        )
        return user
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    def validate(self,data):
        user=authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Cred")
    
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Products
        fields="__all__"
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields="__all__"
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields="__all__"
class BillingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=BillingAddress
        fields="__all__"
class CoupanSerializer(serializers.ModelSerializer):
    class Meta:
        model=Coupan
        fields="__all__"
