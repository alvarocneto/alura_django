from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Perfil (models.Model):
    """Modelo do Perfil"""
    nome = models.CharField(max_length=255, null=False)
    telefone = models.CharField(max_length=15, null=False)
    nome_empresa = models.CharField(max_length=255, null=False)
    contatos = models.ManyToManyField('self')
    usuario = models.OneToOneField(User, related_name="perfil")

    @property
    def email(self):
        return self.usuario.email

    def convidar(self, perfil_convidado):
        convite = Convite(solicitante=self, convidado=perfil_convidado)
        convite.save()  # TODO Bug do convite...


class Convite(models.Model):
    solicitante = models.ForeignKey(Perfil, related_name='convites_feitos')
    convidado = models.ForeignKey(Perfil, related_name='convites_recebidos')

    def aceitar(self):
        self.convidado.contatos.add(self.solicitante)
        self.solicitante.contatos.add(self.convidado)
        self.delete()
