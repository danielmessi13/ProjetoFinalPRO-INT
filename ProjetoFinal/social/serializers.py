from rest_framework import serializers

from social.models import Usuario


class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ('nome', 'telefone', 'sexo')