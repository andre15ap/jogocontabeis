
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from core.views import IndexView, ComecarView, PertuntasView, PontuacaoListView,UsuarioCriarView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', IndexView.as_view(), name='index'),
    path('comecar/<int:pk>', ComecarView.as_view(), name='comecar'),
    path('pergunta/<int:pk>/<int:r>', PertuntasView.as_view(), name='pergunta'),
    path('classificacao/<int:pk>', PontuacaoListView.as_view(), name='pontuacao_list'),
    
    path('entrar',LoginView.as_view(), name='login'),
    path('registrar',UsuarioCriarView.as_view(), name='registrar'),
    path('sair',LogoutView.as_view(), name='logout')
]
