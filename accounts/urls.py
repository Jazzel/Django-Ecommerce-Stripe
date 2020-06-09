from django.urls import path
from .views import (ProfileView, UserRegisterView,
                    UserDetailsEditView, UserLogListView, UserLogDetailView, UserListView, UserDetailView)
from django.contrib.auth import views as auth_views

app_name = 'profiles'

urlpatterns = [
    path('user-profile/', UserDetailsEditView, name='profile'),
    path('registration/', UserRegisterView.as_view(), name='registration'),
    path('user-log/', UserLogListView.as_view(), name='user_log'),
    path('user-log/details/<int:pk>',
         UserLogDetailView.as_view(), name='user_log_details'),
    path('users/', UserListView.as_view(), name='users'),
    path('user_details/<int:pk>', UserDetailView.as_view(), name='user_details'),
]
