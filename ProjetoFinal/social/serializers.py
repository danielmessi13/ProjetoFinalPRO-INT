from rest_framework import serializers
from social.models import Postagem


class PostagemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Postagem
        fields = ('url', 'texto', 'data')
