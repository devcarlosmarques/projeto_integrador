from django.views.generic import CreateView, ListView, TemplateView, FormView, RedirectView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Paciente, Medico, Consulta
from .forms import PacienteForm, MedicoForm, ConsultaForm
from django.views import View
from .forms import LoginForm, RegistroForm
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(FormView):
    template_name = 'pages/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Usuário ou senha inválidos.')
            return self.form_invalid(form)


class LogoutView(RedirectView):
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class RegistroView(FormView):
    template_name = 'pages/registro.html'
    form_class = RegistroForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'Usuário registrado com sucesso.')
        return super().form_valid(form)

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_medicos'] = Medico.objects.count()
        context['total_pacientes'] = Paciente.objects.count()
        context['total_consultas'] = Consulta.objects.count()
        return context

class PacienteCreateView(CreateView):
    model = Paciente
    form_class = PacienteForm
    template_name = 'pages/paciente_form.html'
    success_url = reverse_lazy('listar_pacientes')

class MedicoCreateView(CreateView):
    model = Medico
    form_class = MedicoForm
    template_name = 'pages/medico_form.html'
    success_url = reverse_lazy('listar_medicos')

class PacienteListView(ListView):
    model = Paciente
    template_name = 'pages/paciente_list.html'
    context_object_name = 'pacientes'

class MedicoListView(ListView):
    model = Medico
    template_name = 'pages/medico_list.html'
    context_object_name = 'medicos'

class ConsultaCreateView(TemplateView):
    template_name = 'pages/consulta_form.html'

    def get(self, request, *args, **kwargs):
        form = ConsultaForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = ConsultaForm(request.POST)

        if form.is_valid():
            # Obtém o paciente a partir do formulário
            paciente_id = request.POST.get('paciente')
            paciente = Paciente.objects.get(id=paciente_id)

            # Obtém o médico a partir do formulário
            medico_id = request.POST.get('medico')
            medico = Medico.objects.get(id=medico_id)

            # Cria a instância de consulta sem salvar imediatamente
            consulta = form.save(commit=False)
            consulta.paciente = paciente  # Atribui o paciente à consulta
            consulta.medico = medico  # Atribui o médico à consulta

            # Atribui a data da consulta
            consulta.data = form.cleaned_data['data']

            consulta.save()  # Salva a consulta
            return redirect('listar_consultas')  # Redireciona para a página de listagem de consultas

        # Se o formulário não for válido, retorna com erro
        return render(request, self.template_name, {'form': form})


class ConsultaListView(ListView):
    model = Consulta
    template_name = 'pages/consulta_list.html'
    context_object_name = 'consultas'

class GetPacienteNomeView(View):
    def get(self, request):
        cpf = request.GET.get('cpf')
        paciente = Paciente.objects.filter(cpf=cpf).first()
        if paciente:
            return JsonResponse({'nome': paciente.nome, 'id': paciente.id})
        return JsonResponse({'error': 'Paciente não encontrado'}, status=404)
