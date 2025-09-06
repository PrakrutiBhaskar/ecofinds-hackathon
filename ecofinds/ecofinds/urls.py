from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # auth
    path("signup/", views.signup, name="signup"),
    path("login/",  auth_views.LoginView.as_view(template_name="marketplace/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # user
    path("dashboard/", views.dashboard, name="dashboard"),

    # products
    path("", views.product_list, name="product_list"),
    path("products/new/", views.product_create, name="product_create"),
    path("products/mine/", views.my_listings, name="my_listings"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:pk>/edit/", views.product_update, name="product_update"),
    path("products/<int:pk>/delete/", views.product_delete, name="product_delete"),

    # cart & purchases
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("purchases/", views.purchases, name="purchases"),
]
