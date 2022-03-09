"""chatbot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.http import HttpResponseRedirect

from gestion.views import ReferidosListado, ReferidoDetalle, ReferitosCrear, ReferitoEliminar, ReferidoActualizar, \
    ConvenioListado, ConvenioDetalle, ConvenioCrear, ConvenioEliminar, ConvenioActualizar, ConvenioPendiente, ConvenioRevisar, ConvenioRevisados

from django.conf import settings
from django.urls import include, path
from django.contrib import admin
from gestion.views import index

from django.conf.urls import include, url


urlpatterns = [
    path('debug/', index),
    path('', lambda r: HttpResponseRedirect('conveniocda/')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),

    # La ruta 'leer' en donde listamos todos los registros o postres de la Base de Datos
    path('referidos/', ReferidosListado.as_view(template_name="referidos/index.html"), name='leer'),

    # La ruta 'detalles' en donde mostraremos una página con los detalles de un postre o registro
    path('referidos/detalle/<int:pk>', ReferidoDetalle.as_view(template_name="referidos/detalles.html"), name='detalles'),

    # La ruta 'crear' en donde mostraremos un formulario para crear un nuevo postre o registro
    path('referidos/crear', ReferitosCrear.as_view(template_name="referidos/crear.html"), name='crear'),

    # La ruta 'actualizar' en donde mostraremos un formulario para actualizar un postre o registro de la Base de Datos
    path('referidos/editar/<int:pk>', ReferidoActualizar.as_view(template_name="referidos/actualizar.html"),
         name='actualizar'),

    # La ruta 'eliminar' que usaremos para eliminar un postre o registro de la Base de Datos
    path('referidos/eliminar/<int:pk>', ReferitoEliminar.as_view(), name='eliminar'),

    path('conveniocda/', ConvenioListado.as_view(template_name="conveniocda/index.html"), name='leer'),
    # La ruta 'detalles' en donde mostraremos una página con los detalles de un postre o registro
    path('conveniocda/detalle/<int:pk>', ConvenioDetalle.as_view(template_name="conveniocda/detalles.html"), name='detalles'),
    # La ruta 'crear' en donde mostraremos un formulario para crear un nuevo postre o registro
    path('conveniocda/crear', ConvenioCrear.as_view(template_name="conveniocda/crear.html"), name='crear'),
    # La ruta 'actualizar' en donde mostraremos un formulario para actualizar un postre o registro de la Base de Datos
    path('conveniocda/editar/<int:pk>', ConvenioActualizar.as_view(template_name="conveniocda/actualizar.html"),
         name='actualizar'),
    # La ruta 'eliminar' que usaremos para eliminar un postre o registro de la Base de Datos
    path('conveniocda/eliminar/<int:pk>', ConvenioEliminar.as_view(), name='eliminar'),

    path('conveniopendientes/', ConvenioPendiente.as_view(template_name="conveniopendientes/index.html"), name='pendientes'),
    path('conveniopendientes/revisados', ConvenioRevisados.as_view(template_name="conveniopendientes/revisados.html"), name='revisados'),

    path('conveniopendientes/detalle/<int:pk>', ConvenioDetalle.as_view(template_name="conveniopendientes/detalles.html"),
         name='detallespendiente'),
    path('conveniopendientes/revisar/<int:pk>', ConvenioRevisar.as_view(template_name="conveniopendientes/revisar.html"),
         name='revisar'),
]
# Add Django Debug Toolbar
if settings.DEBUG:
    import debug_toolbar
    urlpatterns +=[
        path('/__debug__/', include(debug_toolbar.urls)),
    ]
