from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from usuarios.views import *
from django.contrib.auth import views as v

urlpatterns = [
    path('home/', index, name='home'),
    path('', index, name='home'),
    path('postar/', postar, name='postar'),
    path('postagem/<int:id>/editar', postar_editar, name='postagem_editar'),
    path('postagem/<int:id>/deletar', postar_deletar, name='postagem_deletar'),
    path('pesquisar/amigo', pesquisar_amigo, name='pesquisar_amigo'),
    path('usuario/<int:id>', perfil_usuario, name='perfil_usuario'),
    path('convidar/<int:id>', convidar, name='convidar'),
    path('bloquear/<int:id>', bloquear, name='bloquear'),
    path('desbloquear/<int:id>', desbloquear, name='desbloquear'),
    path('amigos/convites', convites, name='convites'),
    path('amigos/convites/cancelar/<int:id>', cancelar_convite, name='cancelar_convite'),
    path('amigos/convites/aceitar/<int:id>', aceitar, name='aceitar'),
    path('amigos/convites/rejeitar/<int:id>', rejeitar, name='rejeitar'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),
    path('perfil/alterar_senha/', alterar_senha, name='alterar_senha'),
    path('amigos/convites/desfazer/<int:id>', desfazer, name='desfazer'),
    path('cadastrar/', RegistrarUsuarioView.as_view(), name='cadastrar'),
    path('listar/', listar_usuario, name='listar'),
    path('desativar/', desativar, name='desativar_perfil'),
    path('ativar_perfil/<int:id>', ativar_perfil, name='ativar_perfil'),
    path('ativar/<int:id>', ativar, name='ativar'),
    path('listar/<int:id>', super_mudanca, name='mudar'),
    path('login/', LoginCustom.as_view(template_name='login.html'), name='login'),
    path('logout/', v.LogoutView.as_view(template_name='login.html'), name='logout'),
    path('password_reset/$', v.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='password_reset'),
    path('password_reset/done/$', v.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/$',
         v.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/$', v.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
