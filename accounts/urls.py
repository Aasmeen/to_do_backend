from django.urls import path
from rest_framework.authtoken import views

from accounts.views import LogoutAPIView, RegisterAPIView

urlpatterns = [
    path('login/', views.obtain_auth_token, name="login"),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    path('register/', RegisterAPIView.as_view(), name="register")
]
