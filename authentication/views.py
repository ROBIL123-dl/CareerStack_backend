from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .serializers import EmailSerializer,VerifySerializer,RegisterSerializer,LoginSerializer
from .services import send_otp,send_to_verify_otp


class CheckEmailAPIView(APIView):
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

   
class Verify_OTP(APIView):
       def post(self,request):
           serializer = VerifySerializer(data=request.data)
           if serializer.is_valid():
                print("entere..k'd\ok\v;l")
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
           
class Register(APIView):
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
    
    

class Login(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            response =  Response({"message":"token Created"
            }, status=status.HTTP_200_OK)
            
            response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,       # True in production (HTTPS)
            samesite='Strict',
            max_age=300 #5min
            )

            response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Strict',
            max_age=86400
           )

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            raise AuthenticationFailed("No refresh token")

        refresh = RefreshToken(refresh_token)
        access = refresh.access_token

        response = Response({"message": "Token refreshed"},status=status.HTTP_200_OK)

        response.set_cookie(
            key='access_token',
            value=str(access),
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=300 #5min
        )

        return response

    
class Logout(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"})
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response


