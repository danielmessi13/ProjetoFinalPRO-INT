from django.db import models
from django.utils import timezone
from itertools import chain
from django.contrib.auth.models import User


# Create your models here.
class Usuario(models.Model):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    )

    nome = models.CharField(max_length=128, null=False)
    telefone = models.CharField(max_length=20, null=False)
    foto = models.ImageField(upload_to='profiles', default='profiles/user.png')
    sexo = models.CharField(choices=SEXO_CHOICES, null=False, max_length=12)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    bloqueados = models.ManyToManyField('Usuario', related_name='usuarios_bloqueados')
    amigos = models.ManyToManyField('Usuario', related_name='amigos_usuario')

    @property
    def email(self):
        return self.user.email

    def convidar(self, perfil_convidado):
        Convite.objects.create(convidado=perfil_convidado, solicitante=self)

    def bloquear(self, perfil_a_bloquear):
        self.bloqueados.add(perfil_a_bloquear)

    def desbloquear(self, perfil_a_desbloquear):
        self.bloqueados.remove(perfil_a_desbloquear)

    def timeline(self):
        posts = list(self.usuario_postagem.filter())
        if self.amigos_usuario.all():
            for amigo in self.amigos_usuario.all():
                posts += list(amigo.usuario_postagem.filter())
        return sorted(chain(posts), key=lambda instance: instance.data, reverse=True)

    def __str__(self):
        return self.user.username

    def desativar(self, motivo):
        Desativo.objects.create(user=self, motivo=motivo)
        self.user.is_active = 0
        self.user.save()

    def ativar(self):
        print('deu bm')
        self.desativacao.delete()
        self.user.is_active = 1
        self.user.save()


class PostagemCompartilhada(models.Model):
    usuario = models.ForeignKey(Usuario, related_name='usuario_compartilhada', on_delete=models.CASCADE)
    postagem = models.ForeignKey('Postagem', related_name='postagem_compartilhada', on_delete=models.CASCADE)


class Storie(models.Model):
    stories = models.ImageField(upload_to='stories')
    usuario = models.ForeignKey(Usuario, related_name='stories_usuario', on_delete=models.CASCADE)
    data = models.DateTimeField(default=timezone.now)


class Anexo(models.Model):
    TIPOS = (
        ('I', 'imagem'),
        ('P', 'pdf'),
    )

    arquivo = models.FileField(upload_to='anexos')
    tipo = models.CharField(max_length=30, choices=TIPOS)
    postagem = models.ForeignKey('Postagem', related_name='anexo_postagem', on_delete=models.CASCADE, null=True,
                                 blank=True)


class Comentario(models.Model):
    texto_comentario = models.TextField()
    data = models.DateField(default=timezone.now)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_comentario')
    postagem = models.ForeignKey('Postagem', on_delete=models.CASCADE, related_name='postagem_comentario')


class Reacao(models.Model):
    TIPOS = (
        ('L', 'like'),
        ('D', 'dislike'),
    )

    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    postagem = models.ForeignKey('Postagem', on_delete=models.CASCADE)
    tipo_reacao = models.CharField(max_length=30, choices=TIPOS)


class Mensagem(models.Model):
    emissor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='emissor')
    receptor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='receptor')
    texto_mensagem = models.TextField()
    lida = models.BooleanField(default=False)


class Postagem(models.Model):
    texto = models.TextField()
    data = models.DateTimeField(default=timezone.now)
    usuario = models.ForeignKey(Usuario, related_name='usuario_postagem', on_delete=models.CASCADE)
    compartilhada = models.BooleanField(default=False)
    data_compartilhada = models.DateTimeField(default=timezone.now)
    compartilhador = models.ForeignKey(Usuario, related_name='usuario_compartilhador', on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return self.texto


class Convite(models.Model):
    convidado = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='convites_recebidos')
    solicitante = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='convites_feitos')

    def aceitar(self):
        self.convidado.amigos.add(self.solicitante)
        self.solicitante.amigos.add(self.convidado)
        self.delete()

    def recusar(self):
        self.delete()


class Desativo(models.Model):
    user = models.OneToOneField(Usuario, related_name='desativacao', on_delete=models.CASCADE)
    motivo = models.TextField()

    def __str__(self):
        return self.motivo
