# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Referidos, Conveniocda, EmpresaUsuario
from django.urls import reverse

from django.contrib import messages

from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms

from django.shortcuts import render

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

class ConvenioListado(LoginRequiredMixin, ListView):
    model = Conveniocda
    paginate_by = 10
    context_object_name = 'convenio'

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            # el usuario no está logueado, ir a la página de login
            return super(ConvenioListado, self).get_login_url()
        # El usuario está logueado pero no está autorizado
        return '/no_autorizado/'

    def test_func(self):
        # obtenemos todos los grupos del usuario logueado
        grupos = self.request.user.groups.all()
        # comparamos que el usuario pertenezca al grupo VENDEDOR o SUPERVISOR
        for grupo in grupos:
            if grupo in ['CDA', 'SUPERVISOR']:
                return True
        return False

    def get_queryset(self):
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

#    def get_context_data(self, **kwargs):
#        context = super(ConvenioListado, self).get_context_data(**kwargs)
#        context['filter'] = self.request.GET.get('filter', 'give-default-value')
#        return context

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
    fields = ['nombre', 'apellido', 'documento', 'telefono','placa', 'chasis','tipodocumento','tipovehiculo', 'revision']
    success_message = "Convenio cda creado correctamente"

    def form_valid(self, form):
        idEmp = EmpresaUsuario.objects.filter(usuario=self.request.user).values_list(
            'empresa__id', flat=True).first()
        form.id_estado = 1
        form.id_empresa = idEmp
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pendientes')

class ConvenioDetalle(LoginRequiredMixin, DetailView):
    model = Conveniocda

class ConvenioActualizar(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Conveniocda
    form = Conveniocda
    fields = ['nombre', 'apellido', 'documento', 'telefono', 'placa', 'chasis', 'valor', 'tipodocumento',
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
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['estado'].required = False
            self.fields['estado'].widget.attrs['disabled'] = False

    class Meta:
        model = Conveniocda
        fields = ['valor', 'estado', 'observaciones']

def clean_estado(self):
    return self.initial['estado']

class ConvenioRevisar(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Conveniocda
    #form = Conveniocda
    form_class = UserForm
    #fields = ['valor', 'estado', 'observaciones']
    initial = {'estado': '4'}
    #disabled_fields = ('estado',)
    success_message = 'Se registró la revisión satisfactoriamente'

    def get_context_data(self, **kwargs):
        context = super(ConvenioRevisar, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'give-default-value')
        return context

    def form_valid(self, form):
        self.object.estado_id = 4
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('revisados')