import re
from rest_framework import serializers
from .models import User



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
    email = EmailSerializer()
    otp = serializers.RegexField(
        regex=r'^\d{4}$',
        error_messages={
            "invalid": "OTP must be a 4-digit number"
        }
    )