from django.conf import settings
from datetime import date

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from .forms import *


# Create your views here.

@login_required
def index(request):
    return render(request, 'home.html')


@login_required
def postar(request):
    if request.method == "POST":
        form = PostagemForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.usuario = usuario_logado(request)
            model_instance.save()
            tipo = request.POST['tipo']
            if tipo:
                if tipo == 'P':
                    request.FILES['arquivo'] = request.FILES['pdf']
                elif tipo == 'I':
                    request.FILES['arquivo'] = request.FILES['imagem']
                anexo = AnexoForm(request.POST, request.FILES)
                if anexo.is_valid():
                    anexo_instance = anexo.save(commit=False)
                    anexo_instance.postagem = model_instance
                    anexo_instance.save()
                else:
                    print(anexo.errors)
        else:
            print(form.errors)
    return redirect('home')


@login_required
def postar_editar(request, id):
    postagem = get_object_or_404(Postagem, id=id)
    if request.method == "POST":
        form = PostagemForm(request.POST, instance=postagem)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.usuario = usuario_logado(request)
            model_instance.save()
        else:
            print(form.errors)
    return redirect('home')


@login_required
def postar_deletar(request, id):
    postagem = Postagem.objects.get(id=id)
    print(postagem.delete())
    return redirect('home')


@login_required
def pesquisar_amigo(request):
    pesquisa = request.GET['q']
    usuario = usuario_logado(request)

    resultado = Usuario \
        .objects \
        .filter(nome__contains=pesquisa) \
        .exclude(nome=usuario.nome) \
        .exclude(amigos=usuario)

    convites = Convite.objects.filter(solicitante=usuario, convidado__in=resultado)

    resultado = resultado.filter(bloqueados__in=usuario.bloqueados.all())

    if convites:
        resultado = resultado.exclude(nome=convites.all()[0].convidado.nome)

    context = {
        "usuario": usuario_logado(request),
        "resultado": resultado,
        "pesquisa": pesquisa
    }
    return render(request, 'pesquisa.html', context)


@login_required
def usuario_logado(request):
    return request.user.perfil


@login_required
def convidar(request, id):
    perfil_a_convidar = Usuario.objects.get(id=id)
    perfil_logado = usuario_logado(request)
    perfil_logado.convidar(perfil_a_convidar)
    return redirect('home')


@login_required
def convites(request):
    usuario = usuario_logado(request)
    convites = usuario.convites_recebidos.all()
    amigos = usuario.amigos.all()

    context = {
        "convites": convites,
        "amigos": amigos
    }

    return render(request, 'amigos.html', context)


@login_required
def aceitar(request, id):
    convite = Convite.objects.get(id=id)
    convite.aceitar()
    return redirect('home')


@login_required
def rejeitar(request, id):
    convite = Convite.objects.get(id=id)
    convite.recusar()
    return redirect('home')


@login_required
def editar_perfil(request):
    form_senha = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form_editar = UsuarioForm(request.POST)
        form_senha = PasswordChangeForm(user=request.user, data=request.POST)

        if form_senha.is_valid():
            form_senha.save()
            update_session_auth_hash(request, form_senha.user)

        if form_editar.is_valid():
            dados_form = form_editar.cleaned_data
            user = request.user
            user.email = dados_form['email']
            user.username = dados_form['email']
            user.save()
            del (form_editar.cleaned_data['email'])
            perfil = Usuario(**form_editar.cleaned_data)

            perfil.id = request.user.perfil.id
            perfil.user = request.user

            perfil.save()

            return redirect('home')


    else:
        perfil = request.user.perfil.__dict__
        user = {
            'email': request.user.email
        }

        perfil.update(user)
        form_editar = UsuarioForm(initial=perfil)

    context = {
        'form': form_senha,
        'form_editar': form_editar,
        'btn_name': 'Alterar'
    }
    return render(request, 'perfil.html', context)


@login_required
def desfazer(request, id):
    usuario = usuario_logado(request)
    usuario.amigos.remove(id)
    amigo = Usuario.objects.get(id=id)
    amigo.amigos.remove(usuario.id)
    return redirect('convites')


@login_required
def bloquear(request, id):
    bloquear = Usuario.objects.get(id=id)
    usuario = usuario_logado(request)
    usuario.bloquear(bloquear)

    return desfazer(request, bloquear.id)


def esqueceu(request):
    if request.method == "POST":
        form = EnviarForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            send_mail(
                'Subject here',
                'https://www.youtube.com/',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            print(request.POST["email"])

        else:
            print(form.errors)
    return render(request, 'esqueceu.html')
