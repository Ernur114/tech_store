from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from clients.views import login_page, register_page
from tech_store.views import home_view, category_detail, product_detail, cart, catalog_view, add_to_cart, search_view
from tech_store.views import manage_products, manage_product_create, manage_product_edit, manage_product_delete
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def logout_view(request):
    logout(request)
    return redirect('home')

schema_view = get_schema_view(
    openapi.Info(
        title="Tech Store API",
        default_version='v1',
        description="API магазина бытовой техники",
        contact=openapi.Contact(email="support@techstore.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('catalog/', catalog_view, name='catalog'),
    path('search/', search_view, name='product_search'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('category/<slug:slug>/', category_detail, name='category-detail'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('cart/', cart, name='cart'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_page, name='login-short'),
    path('register/', register_page, name='register-short'),
    path('api/clients/', include('clients.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
        path('manage/products/', manage_products, name='manage_products'),
        path('manage/products/new/', manage_product_create, name='manage_product_create'),
        path('manage/products/<int:pk>/edit/', manage_product_edit, name='manage_product_edit'),
        path('manage/products/<int:pk>/delete/', manage_product_delete, name='manage_product_delete'),
]


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Введите токен в формате: Bearer <your_access_token>',
        }
    }
}

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
