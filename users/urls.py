from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name = 'login'),
    path('register/', views.register_page, name = 'register'),
    path('logout/', views.logout_page, name = 'logout'),
    path('activate/<str:email_token>/', views.activate_profile, name = 'activate'),
    path('cart/', views.cart, name = 'cart'),
    path('add-to-cart/<str:uid>/', views.add_to_cart, name = 'add_to_cart'),
    path('remove-item/<str:uid>/', views.remove_from_cart, name = 'remove_from_cart'),
    path('confirm-order/<str:uid>/', views.confirm_order, name = 'confirm_order'),
    path('update-profile/', views.update_profile, name = 'update_profile')
]
