from django import forms
from django.contrib.auth.models import User


class RegistrarUsuarioForm(forms.Form):
    SEXO_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outros'),
    )

    nome = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(required=True)
    telefone = forms.CharField(required=True)
    sexo = forms.CharField(widget=forms.Select(choices=SEXO_CHOICES), required=True)

    def is_valid(self):
        valid = True
        if not super(RegistrarUsuarioForm, self).is_valid():
            self.adiciona_erro('Por favor, verifique os dados informados')
            valid = False

        user_exists = User.objects.filter(username=self.cleaned_data['nome']).exists()
        if user_exists:
            self.adiciona_erro('Usuario já existe')
            valid = False

        return valid

    def adiciona_erro(self, mensagem):
        errors = self._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.utils.ErrorList())
        errors.append(mensagem)
