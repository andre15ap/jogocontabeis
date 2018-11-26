from django import forms

class UsuarioForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)
    senha = forms.CharField(label='Senha',widget=forms.PasswordInput, max_length=100)

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs = {'class': 'form-control','placeholder':'digite Nome'}
        self.fields['senha'].widget.attrs = {'class': 'form-control','placeholder':'digite uma senha'}