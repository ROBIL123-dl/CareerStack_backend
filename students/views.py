from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsStudent
# Create your views here.

class StudentHomeView(APIView):
    permission_classes = [IsStudent]
    def get(self,request):
        return Response({"message":"Student Home"},status=status.HTTP_200_OK)

