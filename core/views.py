from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.
from django.views.generic import View, TemplateView, CreateView, DetailView, ListView

# # from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import SalaResposta, Pergunta, Resposta, Pontuacao
from .forms import UsuarioForm

from django.contrib.auth.models import User

class IndexView(LoginRequiredMixin, TemplateView):
	template_name = 'index.html'
	
	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		salas = SalaResposta.objects.filter(ativo=True)
		context['salas'] = salas
		return context


class UsuarioCriarView(View):
    def get(self, request, *args, **kwargs):
        form = UsuarioForm()
        context = {
			'form':form
		}
        return render(request, 'registration/registration.html',context)

    def post(self, request, *args, **kwargs):
        form = UsuarioForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            senha = form.cleaned_data['senha']
            usuario_count = User.objects.filter(username=nome).count()
            if usuario_count > 0:
                messages.add_message(self.request, messages.ERROR, 'Nome já cadastrado, tente outro!')
                return HttpResponseRedirect(reverse_lazy("registrar"))
            else:
                try:
                    user = User.objects.create_user(nome, password=senha)
                    user.save()
                    messages.add_message(self.request, messages.SUCCESS, 'Cadastro Relizado com sucesso!')
                except:
                    messages.add_message(self.request, messages.ERROR, 'Algo de Errado não esta Certo!')

        else:
            messages.add_message(self.request, messages.ERROR, 'Algo de Errado não esta Certo!')
        return redirect('index')
	
class ComecarView(LoginRequiredMixin, DetailView):
	model = SalaResposta
	template_name = 'pergunta.html'

	def get_context_data(self, **kwargs):
		context = super(ComecarView, self).get_context_data(**kwargs)
		usuario = context['view'].request.user
		id = self.kwargs['pk']
		sala = SalaResposta.objects.get(id=id)
		pont = Pontuacao.objects.filter(usuario=usuario, sala=sala)
		if pont.count() > 0:
			## para jogar so uma vez
			# participou = True
			# msg =  'Você ja participou dessa sala, vá para outra!'
			# context['msg'] = msg
			# context['participou'] = participou
			# return context
			
			## para continuar jogango 
			for p in pont:
				pontuacao = p
				break
			# print(pontuacao)
			pontuacao.pontos = 0
			pontuacao.perguntas_realizadas.clear()
			pontuacao.respostas_computadas.clear()

		else:
			pontuacao = Pontuacao(usuario=usuario, sala=sala, pontos=0)
		pontuacao.save()

		perguntas = sala.perguntas.all()

		for per in perguntas:
			pergunta = per
			pontuacao.perguntas_realizadas.add(per)
			break
	
		respostas = []
		if pergunta:
			for res in pergunta.respostas.all():
				respostas.append(res)

		q = pontuacao.perguntas_realizadas.count()	
		context['pontuacao'] = pontuacao
		context['pergunta'] = pergunta
		context['respostas'] = respostas
		context['q'] = q

		return context


class PertuntasView(LoginRequiredMixin, DetailView):
	model = Pontuacao
	template_name = 'pergunta.html'

	def get_context_data(self, **kwargs):
		context = super(PertuntasView, self).get_context_data(**kwargs)
		id = self.kwargs['pk']
		r = self.kwargs['r']
		usuario = context['view'].request.user
		
		pontuacao = context['object']
		
		sala = pontuacao.sala
		
		resposta = Resposta.objects.get(id=r)
	

		if resposta.verdade and not resposta in pontuacao.respostas_computadas.all():
			valor = pontuacao.pontos
			valor += 1
			pontuacao.pontos = valor
			pontuacao.save()
	
		
		if not resposta in pontuacao.respostas_computadas.all():
			pontuacao.respostas_computadas.add(resposta)

		
		perguntas = sala.perguntas.all()
		
		
		existe = True
		for per in perguntas:
			existe = False
			if pontuacao.perguntas_realizadas.all():
				if not per in pontuacao.perguntas_realizadas.all():
					pergunta = per
					pontuacao.perguntas_realizadas.add(per)
					existe = True
					break
					
			else:
				pergunta = per
				pontuacao.perguntas_realizadas.add(per)
				existe = True
				break

		
		if not existe:
			context['acabou'] = True
			# context['pontos'] = pontuacao.perguntas_realizadas.all().count() - pontuacao.pontos
			context['pontuacao'] = pontuacao

			return context
			
		
		respostas = []
		for res in pergunta.respostas.all():
			respostas.append(res)
	
		q = pontuacao.perguntas_realizadas.count()	
		context['pontuacao'] = pontuacao
		context['pergunta'] = pergunta
		context['respostas'] = respostas
		context['q'] = q

		return context

class PontuacaoListView(LoginRequiredMixin, ListView):
	model = Pontuacao
	template_name = 'pontuacao_list.html'
	
	def get_queryset(self):
		id = self.kwargs['pk']
		return Pontuacao.objects.filter(sala__id=id).order_by('-pontos','usuario__username')

	def get_context_data(self, **kwargs):
		context = super(PontuacaoListView, self).get_context_data(**kwargs)
		id = self.kwargs['pk']
		context['sala'] = SalaResposta.objects.get(id=id)
		return context
