from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import UserProfile, Products, Suppliers, Orders


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'username', 'firstName', 'lastName',
                  'email', 'userType', )


class ProductsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Products
        fields = ('id', 'name', 'supplier_name', 'amount', 'price')
        read_only_fields = ('id',)

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError(
                "Name should be at least 3 characters long.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Price should be greater than zero.")
        return value

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Amount should be greater than zero.")
        return value


class SuppliersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suppliers
        fields = ('id', 'name', 'SupplierEmail', 'Products', 'address', )


class OrdersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Orders
        fields = ('id', 'delivery_name', 'products', 'total_price',
                  'order_date', 'delivery_date', 'address', 'amount', 'status')
