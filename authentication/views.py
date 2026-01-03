from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .Serializers import EmailSerializer,VerifySerializer
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
                email = serializer.validated_data['email']['email']
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
    def post(self,request):
       return Response({"message":"success"},status=201)
    
class Login(APIView):
    def post(self,request):
        return Response({"message":"success"},status=201)
    
class Logout(APIView):
    def get(sef,request):
         return Response({"message":"success"},status=201)


