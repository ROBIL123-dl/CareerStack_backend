import re
from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from rest_framework.exceptions import ValidationError


User = get_user_model()

class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise serializers.ValidationError("Invalid email format!")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email is already registered. Try another!"
            )
        return value
    

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.RegexField(
        regex=r'^\d{4}$',
        error_messages={
            "invalid": "OTP must be a 4-digit number"
        }
    )
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'role',
            'password'
        ]

    
    def validate_first_name(self, value):
        if not re.match(r'^[A-Za-z]{2,50}$', value):
            raise ValidationError(
                "First name must contain only letters and at least 2 characters"
            )
        return value

    
    def validate_last_name(self, value):
        if not re.match(r'^[A-Za-z]{1,50}$', value):
            raise ValidationError(
                "Last name must contain only letters"
            )
        return value

 
    def validate_email(self, value):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, value):
            raise ValidationError("Invalid email format")

        if User.objects.filter(email=value).exists():
            raise ValidationError("Email already registered")

        return value

   
    def validate_role(self, value):
        valid_roles = [choice[0] for choice in User.ROLE_CHOICES]
        if value not in valid_roles:
            raise ValidationError("Invalid role selected")
        return value

   
    def validate_password(self, value):
        password_regex = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@#$%^&+=]{8,}$'
        if not re.match(password_regex, value):
            raise ValidationError(
                "Password must be at least 8 characters, include 1 uppercase letter and 1 number"
            )
        return value

   
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    
    
class LoginSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(write_only=True)
          
        def validate_password(self, value):
             password_regex = r'^(?=.*[A-Z])(?=.*\d)[A-Za-z\d@#$%^&+=]{8,}$'
             if not re.match(password_regex, value):
               raise ValidationError(
                "Password must be at least 8 characters, include 1 uppercase letter and 1 number"
             )
             return value

        def validate(self, data):
          user = authenticate(
            email=data['email'],
            password=data['password']
         )

          if not user:
            raise serializers.ValidationError("Invalid credentials")

          if not user.is_active:
            raise serializers.ValidationError("Account is inactive")

          data['user'] = user
          return data
