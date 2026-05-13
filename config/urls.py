"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from vehiculos.views import VehiculoViewSet, AccesorioViewSet, MarcaViewSet, CompraVehiculoViewSet, UsuarioViewSet, PerfilViewSet, MantenimientoViewSet


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/vehiculos/', VehiculoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/vehiculos/<int:pk>/', VehiculoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('api/accesorios/', AccesorioViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/accesorios/<int:pk>/', AccesorioViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('api/marcas/', MarcaViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/marcas/<int:pk>/', MarcaViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('api/compras/', CompraVehiculoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/compras/<int:pk>/', CompraVehiculoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('api/users/', UsuarioViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/users/<int:pk>/', UsuarioViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('api/perfiles/', PerfilViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/perfiles/<int:pk>/', PerfilViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('api/mantenimiento/', MantenimientoViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('api/mantenimiento/<int:pk>/', MantenimientoViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    })),
    path('api/vehiculos/<int:pk>/comprar/', VehiculoViewSet.as_view({
        'post': 'comprar'
    })),
    #path('api/users/', UserViewSet.as_view()),
]
