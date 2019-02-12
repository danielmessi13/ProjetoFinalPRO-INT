from rest_framework import serializers
from social.models import Postagem
from social.models import Usuario


class PostagemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Postagem
        fields = ('url', 'texto', 'data')


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ('url', 'nome', 'telefone', 'sexo')
