from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, InvalidPage
from .forms import *
from django.db import transaction
import time


# Create your views here.

@login_required
def index(request):
    paginator = Paginator(usuario_logado(request).timeline(), 10)
    page = request.GET.get('page')
    lista = paginator.get_page(page)

    return render(request, 'home.html', {'lista': lista, 'usuario': usuario_logado(request), 'pages': paginator.num_pages})


@login_required
@transaction.atomic
def postar(request):
    if request.method == "POST":
        form = PostagemForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.usuario = usuario_logado(request)
            model_instance.save()
            tipo = request.POST['tipo']
            messages.success(request,"Post criado com sucesso")
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
            messages.error(request, "Erro ao criar o post")

    return redirect('home')


@login_required
@transaction.atomic
def postar_editar(request, id):
    postagem = get_object_or_404(Postagem, id=id)
    if request.method == "POST":
        form = PostagemForm(request.POST, instance=postagem)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.usuario = usuario_logado(request)
            model_instance.save()
            messages.success(request, "Post salvo com sucesso")
        else:
            print(form.errors)
    return redirect('home')


@login_required
@transaction.atomic
def postar_deletar(request, id):
    postagem = Postagem.objects.get(id=id)
    postagem.delete()
    messages.success(request, "Post deletado com sucesso")
    return redirect('home')


@login_required
@transaction.atomic
def pesquisar_amigo(request):
    # messages.add_message(request, messages.INFO, 'Hello world.')
    pesquisa = request.GET['q']
    usuario = usuario_logado(request)

    resultado = Usuario \
        .objects \
        .filter(nome__contains=pesquisa) \
        .exclude(nome=usuario.nome) \
        .exclude(amigos__in=[usuario]) \
        .exclude(usuarios_bloqueados__in=[usuario])

    convites = Convite.objects.filter(solicitante=usuario, convidado__in=resultado)

    filtro = resultado.filter(bloqueados__in=[usuario])

    if filtro:
        resultado = resultado.exclude(bloqueados=usuario)

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
@transaction.atomic
def convidar(request, id):
    perfil_a_convidar = Usuario.objects.get(id=id)
    perfil_logado = usuario_logado(request)
    perfil_logado.convidar(perfil_a_convidar)
    time.sleep(1.2)
    return redirect('home')


@login_required
@transaction.atomic
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
@transaction.atomic
def aceitar(request, id):
    usuario = Usuario.objects.get(id=id)
    convite = Convite.objects.filter(solicitante=usuario, convidado=request.user.perfil)
    convite = convite[0]
    convite.aceitar()
    return redirect('home')


@login_required
@transaction.atomic
def rejeitar(request, id):
    usuario = Usuario.objects.get(id=id)
    convite = Convite.objects.filter(solicitante=usuario, convidado=request.user.perfil)
    convite = convite[0]
    convite.recusar()
    return redirect('home')


@login_required
@transaction.atomic
def cancelar_convite(request, id):
    usuario = Usuario.objects.get(id=id)
    convite = Convite.objects.filter(convidado=usuario, solicitante=request.user.perfil)
    convite = convite[0]
    convite.recusar()
    return redirect('convites')


@login_required
@transaction.atomic
def perfil_usuario(request, id):
    amigo = False
    convidado = False
    convite = False

    usuario = Usuario.objects.get(id=id)
    paginator = Paginator(usuario.timeline(), 10)
    page = request.GET.get('page')
    lista = paginator.get_page(page)

    if usuario == usuario_logado(request):
        return redirect('editar_perfil')

    if usuario.amigos.filter(nome=request.user.perfil.nome):
        amigo = True

    if usuario.convites_recebidos.filter(solicitante=request.user.perfil, convidado=usuario):
        convidado = True

    if usuario.convites_feitos.filter(convidado=request.user.perfil, solicitante=usuario):
        convite = True

    context = {
        'lista': lista,
        'perfil': True,
        'usuario': usuario,
        'amigo': amigo,
        'convite': convite,
        'convidado': convidado,
    }
    return render(request, 'perfil_usuario.html', context)


@login_required
@transaction.atomic
def editar_perfil(request):
    if request.method == 'POST':
        form_editar = UsuarioForm(request.POST)
        form_foto = FotoForm(request.POST, request.FILES)

        if form_editar.is_valid():
            dados_form = form_editar.cleaned_data
            user = request.user
            user.email = dados_form['email']
            user.username = dados_form['email']
            user.save()
            del (form_editar.cleaned_data['email'])
            form_editar.cleaned_data['foto'] = request.user.perfil.foto
            perfil = Usuario(**form_editar.cleaned_data)

            perfil.id = request.user.perfil.id
            perfil.user = request.user

            perfil.save()

            return redirect('editar_perfil')

        if form_foto.is_valid():
            print(form_foto.cleaned_data['foto'])
            request.user.perfil.foto = form_foto.cleaned_data['foto']
            request.user.perfil.save()
            form_foto.save(commit=False)

            return redirect('editar_perfil')

    else:
        form_foto = FotoForm()
        perfil = request.user.perfil.__dict__
        user = {
            'email': request.user.email
        }

        perfil.update(user)
        form_editar = UsuarioForm(initial=perfil)

    context = {
        'form_editar': form_editar,
        'form_foto': form_foto,
        'btn_name': 'Alterar'
    }
    return render(request, 'perfil.html', context)


@login_required
@transaction.atomic
def alterar_senha(request):
    form_senha = PasswordChangeForm(user=request.user)

    if request.method == 'POST':
        form_senha = PasswordChangeForm(user=request.user, data=request.POST)

        if form_senha.is_valid():
            form_senha.save()
            update_session_auth_hash(request, form_senha.user)
            return redirect('alterar_senha')

    context = {
        'form': form_senha,
        'btn_name': 'Alterar'
    }
    return render(request, 'alterar_senha.html', context)


@login_required
@transaction.atomic
def desfazer(request, id):
    usuario = usuario_logado(request)
    usuario.amigos.remove(id)
    amigo = Usuario.objects.get(id=id)
    amigo.amigos.remove(usuario.id)
    return redirect('home')


@login_required
@transaction.atomic
def bloquear(request, id):
    bloquear = Usuario.objects.get(id=id)
    usuario = usuario_logado(request)
    usuario.bloquear(bloquear)

    return desfazer(request, bloquear.id)


@login_required
@transaction.atomic
def desbloquear(request, id):
    bloqueado = Usuario.objects.get(id=id)
    usuario = usuario_logado(request)
    usuario.desbloquear(bloqueado)

    return redirect('convites')


@login_required
@transaction.atomic
def listar_usuario(request):
    if not request.user.is_superuser:
        return render(request, 'forbidden.html')
    usuarios = Usuario.objects.all().exclude(user=request.user)
    return render(request, 'listar_usuarios.html', {'usuarios': usuarios})


@login_required
@transaction.atomic
def super_mudanca(request, id):
    usuario = Usuario.objects.get(id=id)
    if usuario.user.is_superuser:
        usuario.user.is_superuser = False
    else:
        usuario.user.is_superuser = True
    usuario.user.save()

    return redirect('listar')


@login_required
@transaction.atomic
def desativar(request):

    if request.method == 'POST':
        form = DesativarForm(request.POST)
        if form.is_valid():
            motivo = form.cleaned_data['motivo']
            usuario_logado(request).desativar(motivo)

            return redirect('logout')

    return render(request, 'desativar.html')
