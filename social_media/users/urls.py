from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, FollowAPIView, ChangePasswordAPIVIEW

app_name = 'users'

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(),name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('follow', FollowAPIView.as_view(), name='follow'),
    path('change-password', ChangePasswordAPIVIEW.as_view(), name='change_password'),
]
