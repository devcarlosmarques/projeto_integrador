from django.db import models

class Paciente(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField()
    endereco = models.CharField(max_length=100)
    bairro  = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=100)
    crm = models.CharField(max_length=20)
    especialidade = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"

class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    data = models.DateTimeField()

    def __str__(self):
        return f"{self.paciente.nome} com {self.medico.nome} em {self.data.strftime('%d/%m/%Y %H:%M')}"
