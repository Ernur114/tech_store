from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from clients.views import login_page, register_page
from tech_store.views import home, category_detail, product_detail, cart, catalog_view
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
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('catalog/', catalog_view, name='catalog'),
    path('category/<slug:slug>/', category_detail, name='category-detail'),
    path('product/<int:pk>/', product_detail, name='product-detail'),
    path('cart/', cart, name='cart'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_page, name='login-short'),
    path('register/', register_page, name='register-short'),
    path('api/clients/', include('clients.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
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
