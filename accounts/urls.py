from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),  # Login URL
    path('logout/', views.user_logout, name='logout'),  # Logout URL
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard URL
    path('register/', views.register_user, name='register'),  # Registration URL
    path('change-password/', views.change_password, name='change_password'),  # Password change URL
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]
