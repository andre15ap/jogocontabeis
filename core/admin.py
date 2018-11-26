from django.contrib import admin

from .models import Pergunta, Resposta, SalaResposta, AreaConhecimento, Pontuacao
# Register your models here.

admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(SalaResposta)
admin.site.register(AreaConhecimento)
admin.site.register(Pontuacao)