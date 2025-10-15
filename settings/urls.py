from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from clients.views import login_page, register_page
from django.conf import settings
from django.conf.urls.static import static
from tech_store.views import home, product_detail, cart
from django.contrib.auth import logout
from django.shortcuts import redirect

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
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('product/<int:pk>/', product_detail, name='product-detail'),
    path('cart/', cart, name='cart'),
    path('api/clients/', include('clients.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),
    path('login/', login_page, name='login-short'),
    path('register/', register_page, name='register-short'),
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
