from django.db.models import fields
from rest_framework import serializers
from .models import ecommerceUser

class ecommerceUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ecommerceUser
        fields = ['id','username','telephone','address','email','password']