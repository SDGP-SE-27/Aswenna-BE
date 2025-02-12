# from rest_framework import serializers
# from django.contrib.auth import get_user_model

# User = get_user_model()  # ✅ Ensure correct user model

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ['username', 'email', 'phone_number', 'address', 'district', 'password']

#     def create(self, validated_data):
#         password = validated_data.pop('password')  # ✅ Remove password before creating user
#         user = User.objects.create(**validated_data)
#         user.set_password(password)  # ✅ Hash password
#         user.save()
#         return user



# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)


from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'address', 'district', 'role', 'password']  # ✅ Added "role"

    def validate_role(self, value):
        if value not in ['farmer', 'seller']:
            raise serializers.ValidationError("Invalid role. Choose 'farmer' or 'seller'.")
        return value    

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)  # ✅ Hash password
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
