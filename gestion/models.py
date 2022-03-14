from django.conf import settings
from django.db import models
from django.forms import ModelForm
from django.utils import timezone
# Create your models here.

class Estados(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'estados'

class Fechasrevision(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.CharField(max_length=10)

    def __str__(self):
        return self.fecha

    class Meta:
        db_table = 'fechasrevision'


class Empresas(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'empresas'

class TiposVehiculo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tiposvehiculos'

class TiposDocumento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    estado = models.ForeignKey(Estados, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'tiposdocumento'

class Clientes(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    documento = models.CharField(max_length=100)
    tipoDocumento = models.ForeignKey(TiposDocumento, default=1, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados, default=1, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=100, null=True)
    ubicacion1 = models.CharField(max_length=200, null=True)
    ubicacion2 = models.CharField(max_length=200, null=True)
    correo = models.CharField(max_length=100, null=True, default='')
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'clientes'

class Referidos(models.Model):
    id = models.AutoField(primary_key=True)
    tipoDocumento = models.ForeignKey(TiposDocumento, default=1, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados, default=1, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    apellido = models.CharField(max_length=200)
    documento = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100, null=True)
    nombreReferido = models.CharField(max_length=200)
    apellidoReferido = models.CharField(max_length=200)
    documentoReferido = models.CharField(max_length=100)
    telefonoReferido = models.CharField(max_length=100, null=True)
    urlFoto1 = models.CharField(max_length=200)
    urlFoto2 = models.CharField(max_length=200)
    observaciones = models.CharField(max_length=500)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now_add=False)

    def __srt__(self):
        return  self.nombre

    class Meta:
        db_table = 'referidos'

class Conveniocda(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    apellido = models.CharField(max_length=100, null=False)
    tipodocumento = models.ForeignKey(TiposDocumento, default=1, on_delete=models.CASCADE)
    tipovehiculo = models.ForeignKey(TiposVehiculo, default=1, on_delete=models.CASCADE)
    documento = models.CharField(max_length=100, null=False)
    estado = models.ForeignKey(Estados, default=1, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=100, null=True)
    placa = models.CharField(max_length=100, null=False)
    empresa = models.ForeignKey(Empresas, default=1, on_delete=models.CASCADE)
    revision = models.ForeignKey(Fechasrevision, default='1', on_delete=models.CASCADE)
    valor = models.CharField(max_length=200, default='$ ')
    observaciones = models.CharField(max_length=500)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    fechaModificacion = models.DateTimeField(auto_now_add=False)
    creador = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.fechaCreacion = timezone.now()
        self.fechaModificacion = timezone.now()
        return super(Conveniocda, self).save(*args, **kwargs)

    def __srt__(self):
        return self.nombre

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'conveniocda'
        unique_together = ('placa', 'revision')
        permissions = (
                        ("CDA", "Permisos CDA"),
                        ("GANE", "Permisos GANE"),
                        ("SUPERGIROS", "Permisos SuperGiros"),
                      )

class Historialconvenios(models.Model):
    id = models.AutoField(primary_key=True)
    convenio = models.ForeignKey(Conveniocda, default=1, on_delete=models.CASCADE)
    estado = models.ForeignKey(Estados, default=1, on_delete=models.CASCADE)
    observaciones = models.CharField(max_length=500)
    fecha = models.DateTimeField(auto_now_add=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

    def __srt__(self):
        return self.id

    class Meta:
        db_table = 'historialconvenios'

class EmpresaUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=False)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresas, default=1, on_delete=models.CASCADE)

    def __srt__(self):
        return self.id

    class Meta:
        db_table = 'empresausuario'

class ConveniosForm(ModelForm):
    class Meta:
        model = Conveniocda
        fields =['nombre', 'apellido','fechaModificacion', 'placa', 'documento']