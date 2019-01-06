from django import forms
from django.core.exceptions import ValidationError

from .models import *


class CadastroForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': "form-control"}),
            'email': forms.TextInput(attrs={'class': "form-control"}),
            'senha': forms.PasswordInput(attrs={'class': "form-control"})
        }


class UsuarioForm(forms.Form):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    )

    nome = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    telefone = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}))
    sexo = forms.CharField(required=True, widget=forms.Select(choices=SEXO_CHOICES, attrs={'class': 'form-control'}))

    def is_valid(self):
        valid = True
        if not super(UsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados informados')
            valid = False

        return valid

    def adiciona_erro(self, mensagem):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(mensagem)

    # def __init__(self, *args, **kwargs):
    #     super(UsuarioForm, self).__init__(*args, **kwargs)
    #     self.initial['nome'] = 'Initial value'


class PostagemForm(forms.ModelForm):
    class Meta:
        model = Postagem
        fields = ["texto"]
        widgets = {
            'texto': forms.TextInput(attrs={'class': "form-control"}),
        }


class FotoForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["foto"]
        widgets = {
            'foto': forms.FileInput(attrs={'class': "form-control"}),
        }


class AnexoForm(forms.ModelForm):
    class Meta:
        model = Anexo
        fields = ["arquivo", "tipo"]
        widgets = {
            'arquivo': forms.FileInput(attrs={'class': "form-control"}),
        }


class EnviarForm(forms.Form):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
