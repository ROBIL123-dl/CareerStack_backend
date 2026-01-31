from django.urls import path,include
from . import views

urlpatterns = [
    path('verifyEmail/',views.CheckEmailView.as_view()),
    path('verifyOtp/',views.Verify_OTPView.as_view()),
    
    path('signup/',views.RegisterView.as_view()),
    path('login/',views.LoginView.as_view()),
    path('refresh/', views.RefreshTokenView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    
    path('authStatus/', views.AuthStatusView.as_view()),
    path('csrf/',views.CSRFView.as_view())
]