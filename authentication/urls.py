from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('verifyEmail/',views.CheckEmailAPIView.as_view()),
    path('verifyOtp/',views.Verify_OTP.as_view()),
    
    path('signup/',views.Register.as_view()),
    path('login/',views.Login.as_view()),
    path('refresh/', views.RefreshTokenView.as_view())
]