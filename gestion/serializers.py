from django.contrib.auth.models import User, Group
from .models import Conveniocda, Empresas, TiposDocumento
from rest_framework import serializers

class ConveniosSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Conveniocda
        #exclude = ['is_removed', 'created', 'modified']
        fields = ['id', 'nombre', 'apellido', 'placa', 'documento']

class EmpresasSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Empresas
        #exclude = ['is_removed', 'created', 'modified']
        fields = ['id', 'nombre']

class TiposdocumentoSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TiposDocumento
        #exclude = ['is_removed', 'created', 'modified']
        fields = ['id', 'nombre', 'estado_id']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']