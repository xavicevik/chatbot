from django.contrib import admin

# Register your models here.
from .models import Referidos, Estados, TiposDocumento, TiposVehiculo, Conveniocda, Empresas, EmpresaUsuario

#admin.site.register(Referidos)
admin.site.register(Estados)
admin.site.register(TiposDocumento)
admin.site.register(TiposVehiculo)
admin.site.register(Empresas)
admin.site.register(EmpresaUsuario)

class ReferidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'documento', 'telefono', 'estado')
    list_filter = ('estado', 'tipoDocumento')
    search_fields = ('documento','nombre')
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('nombre', 'apellido', 'documento')
        }),
        ('Referido', {
            'fields': ('nombreReferido', 'apellidoReferido', 'documentoReferido')
        }),
    )

class ConvenioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'documento', 'telefono', 'estado', 'placa','chasis','valor','observaciones','fechaCreacion','fechaModificacion','empresa','estado','tipovehiculo','creador')
    list_filter = ('estado', 'tipovehiculo','empresa')
    search_fields = ('documento','nombre','placa')
    list_per_page = 10
    fieldsets = (
        ('Usuario', {
            'fields': ('nombre', 'apellido', 'tipodocumento', 'documento','telefono')
        }),
        ('Vehiculo', {
            'fields': ('tipovehiculo', 'placa', 'chasis', 'valor')
        }),
    )

#admin.site.register(Referidos, ReferidoAdmin)
admin.site.register(Conveniocda, ConvenioAdmin)

admin.site.site_header = "Convenios CDA Admin"
admin.site.site_title = "Convenios CDA titulo"
