from django.urls import path
from . import (
    views, 
    api_views,
    auth_views,
)
from .auth_views import (
    LogoutView, 
    ChangePasswordView,
    ProfileView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # For Login (Generate Access & Refresh Token)
    TokenRefreshView,     # For Refreshing Token
)

urlpatterns = [
    # ---------------- Web URLs ----------------
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),

    path('task/', views.task_form, name='task_form'),
    path('list/', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle_task'),

    # API URLs
    path('api/tasks/', api_views.task_list_create, name='api_task_list_create'),
    path('api/tasks/<int:pk>', api_views.task_detail, name='api_task_detail'),

    # ---------------- JWT Auth APIs ----------------
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # Login - Generate Tokens
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),     # Refresh Token

     # ---------------- Custom Auth APIs ----------------
    path('api/logout/', LogoutView.as_view(), name='token_blacklist'),                # Logout - Blacklist Token
    path('api/change-password/', ChangePasswordView.as_view(), name='change_password'),  # Change Password
    path('api/profile/', ProfileView.as_view(), name='profile'),                      # Get User Profile
]
