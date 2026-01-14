from rest_framework import serializers
from models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    reset_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'phone',
            'username',
            'password',
            'reset_password',
        )

    def validate(self, attrs):
        if attrs['password'] != attrs['reset_password']:
            raise serializers.ValidationError(
                {"password": "Parollar mos emas"}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('reset_password')
        password = validated_data.pop('password')

        user = User(**validated_data)
        user.set_password(password)

        user.is_active = False
        user.save()
        return user

    


    
