from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello_api, name='hello_api'),
    path('register/', views.register_api, name='register_api'),
    path('login/', views.login_api, name='login_api'),
    path('logout/', views.logout_api, name='logout_api'),
    path('profile/', views.profile_api, name='profile_api'),
    path('profile/update/', views.update_profile_api, name='update_profile_api'),
    path('profile/change-password/', views.change_password_api, name='change_password_api'),
    path('home/', views.home_api, name='home_api'),
]