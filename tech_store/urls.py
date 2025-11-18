from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('search/', views.search_view, name='product_search'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('api/categories/', views.CategoryListAPIView.as_view(), name='api_categories'),
    path('api/products/', views.ProductListAPIView.as_view(), name='api_products'),
    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('api/products/search/', views.ProductListAPIView.as_view(), name='api_product_search'),
    path('manage/products/', views.manage_products, name='manage_products'),
    path('manage/products/new/', views.manage_product_create, name='manage_product_create'),
    path('manage/products/<int:pk>/edit/', views.manage_product_edit, name='manage_product_edit'),
    path('manage/products/<int:pk>/delete/', views.manage_product_delete, name='manage_product_delete'),
]
