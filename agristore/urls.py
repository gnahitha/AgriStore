"""
URL configuration for agristore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from store import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.product_list, name='home'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('cart/', views.cart_page, name='cart'),
    path('checkout/', views.checkout_page, name='checkout'),
    path('orders/', views.orders_page, name='orders'),
    path('order-history/', views.order_history, name='order_history'),
    path('product-details/<int:product_id>/', views.product_details, name='product_details'),
    path('product-details/', views.product_details, name='product_details_legacy'),
    path('order-success/', views.order_success, name='order_success'),
    path('increase/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
   path('decrease/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),
   path('clear-cart/', views.clear_cart, name='clear_cart'),
   path('remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
   path('logout/', views.logout_page, name='logout'),
   path("wishlist/", views.wishlist_page, name="wishlist"),
   path(
    "add-to-wishlist/<int:product_id>/",
    views.add_to_wishlist,
    name="add_to_wishlist"
    ),
    path(
    "buy-again/<int:product_id>/",
    views.buy_again,
    name="buy_again"
    ),
    path(
    "cancel-order/<int:order_id>/",
    views.cancel_order,
    name="cancel_order"
    ),
    path("chatbot/", views.chatbot_page, name="chatbot"),
    path(
    "chatbot-response/",
    views.chatbot_response,
    name="chatbot_response"
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.BASE_DIR / "store" / "static"
    )