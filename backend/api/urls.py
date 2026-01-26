from django.urls import path
from . import views

urlpatterns = [
    # Test
    path('hello/', views.hello_api, name='hello_api'),
    
    # Authentification
    path('register/', views.register_api, name='register_api'),
    path('login/', views.login_api, name='login_api'),
    path('logout/', views.logout_api, name='logout_api'),
    
    # Profil utilisateur
    path('profile/', views.profile_api, name='profile_api'),
    path('profile/change-password/', views.change_password_api, name='change_password_api'),
    path('profile/change-language/', views.change_language_api, name='change_language_api'),
    
    # Types de henné
    path('henna-types/', views.henna_types_list_api, name='henna_types_list'),
    path('henna-types/<int:pk>/', views.henna_type_detail_api, name='henna_type_detail'),
    
    # Commandes client
    path('orders/create/', views.create_order_api, name='create_order'),
    path('orders/my-orders/', views.my_orders_api, name='my_orders'),
    path('orders/<int:pk>/', views.order_detail_api, name='order_detail'),
    
    # Dashboard Admin
    path('admin/dashboard/', views.admin_dashboard_api, name='admin_dashboard'),
    path('admin/orders/', views.admin_orders_list_api, name='admin_orders_list'),
    path('admin/orders/<int:pk>/', views.admin_order_detail_api, name='admin_order_detail'),
    path('admin/clients/', views.admin_clients_list_api, name='admin_clients_list'),
]