from rest_framework import serializers
from social.models import Postagem


class PostagemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Postagem
        fields = ('url', 'texto', 'data')


from social.models import Usuario


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nome', 'telefone', 'sexo')