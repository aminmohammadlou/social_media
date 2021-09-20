from django.urls import path
from .views import RegisterAPIView, LoginAPIView, LogoutAPIView, FollowAPIView, ChangePasswordAPIVIEW, FollowingListAPIView, FollowerListAPIView, UserPostsAPIView, UserDetailAPIView
app_name = 'users'

urlpatterns = [
    path('register', RegisterAPIView.as_view(), name='register'),
    path('login', LoginAPIView.as_view(),name='login'),
    path('logout', LogoutAPIView.as_view(), name='logout'),
    path('follow', FollowAPIView.as_view(), name='follow'),
    path('change-password', ChangePasswordAPIVIEW.as_view(), name='change_password'),
    path('<int:pk>/following', FollowingListAPIView.as_view(), name='following'),
    path('<int:pk>/followers', FollowerListAPIView.as_view(), name='followers'),
    path('<int:pk>/posts', UserPostsAPIView.as_view(), name='user_posts'),
    path('<int:pk>/detail', UserDetailAPIView.as_view(), name='user_detail')
]
