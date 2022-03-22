# Create your views here.
import datetime

from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormMixin
from django.http import Http404

from .models import Referidos, Conveniocda, EmpresaUsuario, Empresas, TiposDocumento, Estados, Historialconvenios
from django.urls import reverse

from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, ConveniosSerializers, EmpresasSerializers, TiposdocumentoSerializers
from django.contrib.auth.models import User, Group

from django.conf import settings
from django.core.mail import send_mail

from rest_framework import status
from django.http import Http404

# Add index function to load html file
def index(request):
    return render(request, 'index.html')

class ReferidosListado(ListView):
    model = Referidos
    paginate_by = 10
    context_object_name = 'referidos'

class ReferitosCrear(SuccessMessageMixin, CreateView):
    model = Referidos
    form = Referidos
    fields = "__all__"
    success_message = "Referido creado correctamente"

    def get_success_url(self):
        return reverse('leer')

class ReferidoDetalle(DetailView):
    model = Referidos

class ReferidoActualizar(SuccessMessageMixin, UpdateView):
    model = Referidos
    form = Referidos
    fields = "__all__"
    success_message = 'Referido actualizado correctamente'

    def get_success_url(self):
        return reverse('leer')

class ReferitoEliminar(SuccessMessageMixin, DeleteView):
    model = Referidos
    form = Referidos
    fields = "__all__"

    def get_success_url(self):
        success_message = 'Referido eliminado!'
        messages.success(self.request, (success_message))
        return reverse('leer')



class BuscarConveniosForm(forms.ModelForm):
    nombre = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    apellido = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))
    documento = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Documento'}))
    placa = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Placa'}))
    fecha_inicio = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y', attrs={'placeholder': 'Fecha Inicio'}))
    fecha_fin = forms.DateField(widget=DatePickerInput(format='%m/%d/%Y', attrs={'placeholder': 'Fecha Fin', 'required': 'False'}))

    class Meta:
        model = Conveniocda
        fields = ['nombre', 'apellido', 'documento', 'placa']



class ConvenioListado(LoginRequiredMixin, ListView, FormMixin):
    model = Conveniocda
    paginate_by = 10
    context_object_name = 'convenio'
    form_class = BuscarConveniosForm
    form = BuscarConveniosForm

    def get(self, request, *args, **kwargs):
        print('get')
        self.form = BuscarConveniosForm(self.request.GET or None, )
        return super(ConvenioListado, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print('post')

        self.form = BuscarConveniosForm(self.request.POST or None)

        if self.form.is_valid():
            print(self.form.cleaned_data['nombre'])

            self.object_list = self.get_queryset().filter(nombre__icontains=self.form.cleaned_data['nombre'],
                                                          apellido__icontains=self.form.cleaned_data['apellido'],
                                                          documento__icontains=self.form.cleaned_data['documento'],
                                                          fechaModificacion__gte=self.form.cleaned_data['fecha_inicio'],
                                                          fechaModificacion__lte=self.form.cleaned_data['fecha_fin'])

            #allow_empty = self.get_allow_empty()
            #if not allow_empty and len(self.object_list) == 0:
            #    raise Http404((u"Empty list and '%(class_name)s.allow_empty' is False.")
            #                  % {'class_name': self.__class__.__name__})

            new_context = self.get_context_data(object_list=self.object_list, form=self.form)
            return self.render_to_response(new_context)
        else:
            new_context = self.get_context_data(object_list=self.object_list, form=self.form)
            return self.render_to_response(new_context)
            #raise Http404((u"Empty list and '%(class_name)s.allow_empty' is xxx.")
            #              % {'class_name': self.__class__.__name__})

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            # el usuario no está logueado, ir a la página de login
            return super(ConvenioListado, self).get_login_url()
        # El usuario está logueado pero no está autorizado
        return '/no_autorizado/'

    def _test_func(self):
        # obtenemos todos los grupos del usuario logueado
        grupos = self.request.user.groups.all()
        # comparamos que el usuario pertenezca al grupo VENDEDOR o SUPERVISOR
        for grupo in grupos:
            if grupo in ['CDA', 'SUPERVISOR']:
                return True
        return False

    def _get_queryset(self):
        print('query')
        groups = self.request.user.groups.all().values_list('name', flat=True)
        idEmp = EmpresaUsuario.objects.filter(usuario=self.request.user).values_list(
            'empresa__id', flat=True).first()

        if self.request.GET:
            filter_val = self.request.GET.get('filter', 'give-default-value')
            new_context = Conveniocda.objects.filter(nombre__icontains=filter_val, empresa__id=idEmp) | \
                          Conveniocda.objects.filter(apellido__icontains=filter_val, empresa__id=idEmp) | \
                          Conveniocda.objects.filter(placa__icontains=filter_val, empresa__id=idEmp) | \
                          Conveniocda.objects.filter(documento__icontains=filter_val, empresa__id=idEmp) | \
                          Conveniocda.objects.filter(estado__nombre__icontains=filter_val, empresa__id=idEmp)
        else:
            new_context = Conveniocda.objects.filter(nombre__icontains='', empresa__id=idEmp)

        return new_context



class ConvenioRevisados(LoginRequiredMixin, ListView):
    model = Conveniocda
    paginate_by = 10
    context_object_name = 'convenio'

    def get_queryset(self):
        idEmp = EmpresaUsuario.objects.filter(usuario=self.request.user).values_list(
            'empresa__id', flat=True).first()
        filter_val = self.request.GET.get('filter', 'give-default-value')
        new_context = Conveniocda.objects.filter(estado_id = 4, empresa__id=idEmp)
        return new_context

class ConvenioPendiente(LoginRequiredMixin, ListView):
    model = Conveniocda
    paginate_by = 10
    context_object_name = 'convenio'

    def get_queryset(self):
        idEmp = EmpresaUsuario.objects.filter(usuario=self.request.user).values_list(
            'empresa__id', flat=True).first()
        filter_val = self.request.GET.get('filter', 'give-default-value')
        new_context = Conveniocda.objects.filter(estado_id = 1, empresa__id=idEmp)
        return new_context

#    def get_context_data(self, **kwargs):
#        context = super(ConvenioPendiente, self).get_context_data(**kwargs)
#        context['filter'] = self.request.GET.get('filter', 'give-default-value')
#        return context

class ConvenioCrear(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Conveniocda
    form = Conveniocda
    fields = ['nombre', 'apellido', 'documento', 'telefono','placa','tipodocumento','tipovehiculo', 'revision']
    success_message = "Convenio cda creado correctamente"

    def form_valid(self, form):
        idEmp = EmpresaUsuario.objects.filter(usuario=self.request.user).values_list(
            'empresa__id', flat=True).first()
        userId = User.objects.get(username=self.request.user).pk
        Conveniocda = form.save()
        Conveniocda.save()
        Conveniocda.creador_id = userId
        Conveniocda.estado_id = 1
        Conveniocda.empresa_id = idEmp
        Conveniocda.save()

        historial = Historialconvenios()
        historial.convenio = Conveniocda
        historial.estado = Conveniocda.estado
        historial.observaciones = Conveniocda.observaciones
        historial.fecha = datetime.datetime.now()
        historial.usuario_id = userId
        historial.save()

        #send_mail(
        #    'Subject',
        #    'Message.',
        #    'from@example.com',
        #    ['john@example.com', 'jane@example.com'],
        #    fail_silently=False
        #)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pendientes')

class ConvenioDetalle(LoginRequiredMixin, DetailView):
    model = Conveniocda

class ConvenioActualizar(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Conveniocda
    form = Conveniocda
    fields = ['nombre', 'apellido', 'documento', 'telefono', 'placa', 'valor', 'tipodocumento',
              'tipovehiculo']

    success_message = 'Referido actualizado correctamente'

    def get_success_url(self):
        return reverse('leer')

class ConvenioEliminar(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Conveniocda
    form = Conveniocda
    fields = "__all__"

    def get_success_url(self):
        success_message = 'Convenio eliminado!'
        messages.success(self.request, (success_message))
        return reverse('leer')

class UserForm(forms.ModelForm):

    class Meta:
        model = Conveniocda
        fields = ['valor', 'observaciones']


class ConvenioRevisar(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Conveniocda
    #form = Conveniocda
    form_class = UserForm
    #fields = ['valor', 'estado', 'observaciones']
    #disabled_fields = ('estado',)
    success_message = 'Se registró la revisión satisfactoriamente'

    def get_context_data(self, **kwargs):
        context = super(ConvenioRevisar, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'give-default-value')
        return context

    def form_valid(self, form):
        Conveniocda = form.save()
        Conveniocda.estado = Estados.objects.get(pk=4)
        Conveniocda.save()

        historial = Historialconvenios()
        historial.convenio = Conveniocda
        historial.estado = Conveniocda.estado
        historial.observaciones = Conveniocda.observaciones
        historial.fecha = datetime.datetime.now()
        historial.usuario_id = User.objects.get(username=self.request.user).pk
        historial.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('revisados')

# API Rest
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ConveniosViewSet(viewsets.ModelViewSet):
    queryset = Conveniocda.objects.all()
    serializer_class = ConveniosSerializers
    permission_classes = [permissions.IsAuthenticated]

class EmpresasViewSet(viewsets.ModelViewSet):
    queryset = Empresas.objects.all()
    serializer_class = EmpresasSerializers
    permission_classes = [permissions.IsAuthenticated]

class TiposdocumentosViewSet(viewsets.ModelViewSet):
    queryset = TiposDocumento.objects.all()
    serializer_class = TiposdocumentoSerializers
    #permission_classes = [permissions.IsAuthenticated]