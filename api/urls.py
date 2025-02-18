from django.urls import path, include
from . import views


urlpatterns = [
    # Authentication API
    path('auth/register/', views.RegisterAPIview.as_view()),
    path('auth/login/', views.LoginAPIview.as_view()),
    path('auth/activate-profile/', views.ActivateProfile.as_view()),
    
    # Profile API
    path('profile/', views.ProfileAPIview.as_view()),

    # Products API
    path('products/', views.GetProducts.as_view()),
    path('product/<slug:slug>/', views.GetProduct.as_view()),

    # Cart API
    path('cart/', views.ShowCartAPIview.as_view()),
    path('cart/add-item/', views.AddItemToCartAPIview.as_view()),
    path('cart/remove-item/', views.RemoveItemToCartAPIview.as_view()),
    
]
