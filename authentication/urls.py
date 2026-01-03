from django.urls import path,include
from . import views
urlpatterns = [
    path('verifyEmail/',views.CheckEmailAPIView.as_view()),
    path('verifyOtp/',views.Verify_OTP.as_view())
]