from rest_framework import serializers

from social.models import Postagem


class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Postagem
        fields = ('texto', 'data', 'usuario')
