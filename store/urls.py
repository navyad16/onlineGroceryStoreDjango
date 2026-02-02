from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),

    path('cart/', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    
    path('remove/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('update/<int:product_id>/<str:action>/', views.update_cart, name='update_cart'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),

    path('category/<slug:slug>/', views.category_products, name='category_products'),
]
