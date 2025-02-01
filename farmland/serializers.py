from rest_framework import serializers
from .models import Farmland
from django.contrib.auth import get_user_model

User = get_user_model()

class FarmlandSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)

    class Meta:
        model = Farmland
        fields = [' username' ,'crop_type','land_area']

    def create(self, validated_data):
        username = validated_data.pop('username')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"username": "User not found"})

        farmland = Farmland.objects.create(user=user, **validated_data)
        return farmland