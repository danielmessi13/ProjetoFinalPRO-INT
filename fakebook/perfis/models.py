from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Perfil(models.Model):

    telefone = models.CharField(max_length=20, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('Perfil')
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')

    @property
    def email(self):
        return self.usuario.email

    def __str__(self):
        return self.usuario.username

    def convidar(self, perfil_convidado):

      convite = Convite(solicitante=self, convidado=perfil_convidado)
      convite.save()


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='convites_feitos')
    convidado = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='convites_recebidos')

    def aceitar(self):
        self.solicitante.contatos.add(self.convidado)
        self.convidado.contatos.add(self.solicitante)
        self.delete()
