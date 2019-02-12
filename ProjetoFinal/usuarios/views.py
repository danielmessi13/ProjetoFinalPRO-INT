from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from usuarios.forms import *
from social.models import *
from django.contrib.auth.models import User
from django.views.generic.base import View
from django.contrib import messages
import requests

from requests.exceptions import ConnectionError


class RegistrarUsuarioView(View):
    template_name = 'registrar.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username=dados_form['email'],
                                               email=dados_form['email'],
                                               password=dados_form['senha'])

            Usuario.objects.create(nome=dados_form['nome'], telefone=dados_form['telefone'],
                                   user=usuario, sexo=dados_form['sexo'])

            return redirect('login')

        return render(request, self.template_name, {'form': form})


class LoginCustom(View):
    template_name = 'log in.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST['username']
        senha = request.POST['password']
        user = authenticate(username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('home')

        if getUsuario(request, email):
            return redirect('ativar_perfil', getUsuario(request, email).id)

        return redirect('login')


def ativar_perfil(request, id):
    usuario = User.objects.get(id=id)

    return render(request, 'ativar_perfil.html', {'usuario': usuario})


def ativar(request, id):
    usuario = User.objects.get(id=id)
    usuario.perfil.ativar()
    return redirect('home')


def getUsuario(request, email):
    try:
        usuario = User.objects.all().get(username=email)
        if usuario.is_active == 0:
            return User.objects.all().get(username=email)
        else:
            messages.error(request, 'Senha incorreta')
    except User.DoesNotExist:
        return None
