from django.urls import path
from main.views import *


urlpatterns = [
    path('pacientes/cadastrar/', PacienteCreateView.as_view(), name='cadastrar_paciente'),
    path('medicos/cadastrar/', MedicoCreateView.as_view(), name='cadastrar_medico'),
    path('pacientes/', PacienteListView.as_view(), name='listar_pacientes'),
    path('medicos/', MedicoListView.as_view(), name='listar_medicos'),
    path('consultas/marcar/', ConsultaCreateView.as_view(), name='marcar_consulta'),
    path('consultas/', ConsultaListView.as_view(), name='listar_consultas'),
    path('ajax/get_paciente_nome/', GetPacienteNomeView.as_view(), name='get_paciente_nome'),
    path('home/', HomeView.as_view(), name='home'),
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegistroView.as_view(), name='registro'),
]
