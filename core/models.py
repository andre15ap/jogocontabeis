from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class AreaConhecimento(models.Model):
    nome = models.CharField('Area do conhecimento', max_length=255)
    ativo = models.BooleanField('esta ativa?', default=True)
    
    class Meta:
        verbose_name = 'Area do Conhecimento'
        verbose_name_plural = 'Áreas do conhecimento'

    def __str__(self):
        return self.nome

class Resposta(models.Model):
    texto = models.CharField('texto da resposta', max_length=255)
    verdade = models.BooleanField('a verdadeira?')
    
    def __str__(self):
        return self.texto

    class Meta:
        verbose_name = 'Resposta'
        verbose_name_plural = 'Respostas'


class Pergunta(models.Model):
    texto = models.CharField('texto da pergunta', max_length=255)
    area = models.name = models.ForeignKey(AreaConhecimento, on_delete=models.CASCADE)
    respostas = models.ManyToManyField(Resposta, blank=True)

    class Meta:
        verbose_name = 'Pergunta'
        verbose_name_plural = 'Perguntas'

    def __str__(self):
        return self.texto 


class SalaResposta(models.Model):
    codigo = models.CharField('codigo da sala de resposta', unique=True, max_length=100)
    area = models.ForeignKey(AreaConhecimento, null=True, on_delete=models.SET_NULL)
    perguntas = models.ManyToManyField(Pergunta, blank=True)
    ativo = models.BooleanField('sala ativa?', default=True)

    class Meta:
        verbose_name = 'Sala de Resposta'
        verbose_name_plural = 'Salas de Respostas'

    def __str__(self):
        return self.codigo



class Pontuacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sala = models.ForeignKey(SalaResposta, on_delete=models.CASCADE)
    pontos = models.PositiveIntegerField('pontos', default=0, blank=True)
    perguntas_realizadas = models.ManyToManyField(Pergunta, blank=True, related_name='per_ral')
    respostas_computadas = models.ManyToManyField(Resposta, blank=True, related_name='res_com')
    # questoes = models.PositiveIntegerField('questoes realizadas', default=0, blank=True)

    def __str__(self):
        return '{} - {} pontos '.format(str(self.usuario), self.pontos)

    def total_realizado(self):
        return self.perguntas_realizadas.count()
    