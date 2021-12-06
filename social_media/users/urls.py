from django.urls import path

from .views import (RegisterAPIView, VerifyAPIView, ForgetPasswordAPIView, SetPasswordAPIView, LoginAPIView,
                    FollowAPIView, ChangePasswordAPIVIEW, FollowingListAPIView, FollowerListAPIView, UserDetailAPIView)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('password/forget/', ForgetPasswordAPIView.as_view(), name='forget_password'),
    path('password/set/', SetPasswordAPIView.as_view(), name='set_password'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('password/change/', ChangePasswordAPIVIEW.as_view(), name='change_password'),
    path('follow/', FollowAPIView.as_view(), name='follow'),
    path('<int:pk>/following/', FollowingListAPIView.as_view(), name='following'),
    path('<int:pk>/followers/', FollowerListAPIView.as_view(), name='followers'),
    path('<int:pk>/detail/', UserDetailAPIView.as_view(), name='user_detail'),
]
