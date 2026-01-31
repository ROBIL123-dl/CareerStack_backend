from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import status
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.exceptions import TokenError

from django.utils.decorators import method_decorator
from CareerStack import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .serializers import EmailSerializer,VerifySerializer,RegisterSerializer,LoginSerializer
from .services import send_otp,send_to_verify_otp


class CheckEmailView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_status = send_otp(email)
            if otp_status:
                return Response(
                    {"message": "OTP sent successfully"},
                    status=status.HTTP_200_OK
                )
            return Response(
                {"message": "Failed to send OTP"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            ) 
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

   
class Verify_OTPView(APIView):
       def post(self,request):
           serializer = VerifySerializer(data=request.data)
           if serializer.is_valid():
                email = serializer.validated_data['email']
                otp = serializer.validated_data['otp']
                otp_status = send_to_verify_otp(email,otp)
                if otp_status:
                     return Response(
                    {"message": "Email is verification successfully"},
                    status=status.HTTP_200_OK
                )
                else:
                    return Response(
                    {"message": "Invalid OTP!"},
                    status=status.HTTP_400_BAD_REQUEST
                )
           return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
           )
           
class RegisterView(APIView):
    def post(self, request):
        print("request.data",request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "message": f"User {user.email} created successfully"
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
@method_decorator(csrf_exempt, name="dispatch")
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        response = Response(
            {
                "message": "Token created",
                "data": {
                    "user_id": user.id,
                    "email": user.email,
                    "role": user.role,
                    "status": user.is_blocked,
                },
            },
            status=status.HTTP_200_OK,
        )

        response.set_cookie(
        key="access_token",
        value=str(refresh.access_token),
        httponly=True,
        secure=False,
        samesite="Lax",
        max_age=300,
        path="/",
    )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,    
            samesite="Lax", 
            max_age=7 * 24 * 60 * 60,
           path="/",
        )
        return response


class RefreshTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            raise AuthenticationFailed("Refresh token missing")

        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token
            new_refresh = refresh if settings.SIMPLE_JWT["ROTATE_REFRESH_TOKENS"] else None
        except TokenError:
            raise AuthenticationFailed("Invalid or blacklisted refresh token")

        response = Response({"message": "Token refreshed"})

        response.set_cookie(
            "access_token",
            str(new_access),
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=300,
        )

        if new_refresh:
            response.set_cookie(
                "refresh_token",
                str(new_refresh),
                httponly=True,
                secure=True,
                samesite="Lax",
                max_age=7 * 24 * 60 * 60,
            )

        return response
    
    
class AuthStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user

        return Response(
            {
                   "isAuthenticated": True,
                    "user_id": user.id,
                    "email": user.email,
                    "role": user.role,
                    "status": user.is_blocked,
               
            },
            status=status.HTTP_200_OK,
        )

class CSRFView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({"csrfToken": csrf_token})

    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()   
            except TokenError:
                pass

        response = Response({"message": "Logged out"})
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response



