from django.shortcuts import render, redirect
from usuarios.forms import *
from perfis.models import *
from django.contrib.auth.models import User
from django.views.generic.base import View
# Create your views here.

class RegistrarUsuarioView(View):
    template_name = 'cadastrar.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username=dados_form['nome'],
                                          email=dados_form['email'],
                                          password=dados_form['senha'])

            Perfil.objects.create(telefone=dados_form['telefone'],
                                           nome_empresa=dados_form['nome_empresa'],
                                           usuario=usuario)

            return redirect('login')

        return render(request, self.template_name, {'form': form})