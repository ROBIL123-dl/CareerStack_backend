
import random
from CareerStack.services import send_email
from CareerStack.settings import REDIS_CLIENT
from rest_framework.exceptions import ValidationError, APIException

def generate_otp_int():
    return random.randint(1000, 9999)


def send_otp(email):
    redis_key = f"otp:{email}"

    redis_otp = REDIS_CLIENT.get(redis_key)
    if redis_otp:
        raise ValidationError(
            "OTP already sent. Please enter the OTP or wait before resending."
        )
    try:
        otp = generate_otp_int()
        message = (
            f"Your OTP for email verification is {otp}. "
            f"It will expire in 5 minutes."
        )

        email_status = send_email(email, message)
        if not email_status:
            raise APIException("Failed to send OTP. Please try again later.")

        REDIS_CLIENT.set(redis_key, otp, ex=300)
        return True

    except Exception as e:
        raise APIException("Something went wrong while sending OTP")




def send_to_verify_otp(email, otp):
    try:
        redis_key = f"otp:{email}"
        redis_otp = REDIS_CLIENT.get(redis_key)
        if not redis_otp:
            raise ValidationError("OTP expired or not found")
        if str(otp) != str(redis_otp):
            raise ValidationError("Invalid OTP!")
        REDIS_CLIENT.delete(redis_key)
        return True
    except Exception:
        raise ValidationError("Something went wrong while verifying OTP")