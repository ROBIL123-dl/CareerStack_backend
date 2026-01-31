from django.urls import path

from . import views

urlpatterns = [
    path('home/',views.StudentHomeView.as_view()),
]