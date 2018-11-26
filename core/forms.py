from django import forms

from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
	username = forms.CharField(label='Nome',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Digite seu nome'}))
	password = forms.CharField(label='Senha',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Digite sua senha'}))


class UsuarioForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    senha = forms.CharField(label='Senha',widget=forms.PasswordInput, max_length=100)

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs = {'class': 'form-control','placeholder':'digite Nome'}
        self.fields['senha'].widget.attrs = {'class': 'form-control','placeholder':'digite uma senha'}