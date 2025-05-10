from django import forms
from .models import Paciente, Medico, Consulta
from django.contrib.auth.models import User

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("As senhas não coincidem.")
        return password_confirm
    

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = '__all__'
    
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    endereco = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Digite sua rua'}))
    bairro = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    cidade = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    estado = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = '__all__'
    
    # Adicionando classe bootstrap 'form-control' aos campos
    nome = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    crm = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    especialidade = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['paciente', 'medico', 'data']

    data = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), 
        required=True
    )
