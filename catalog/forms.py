from django import forms
from .models import Venda, ItemVenda
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ['cliente']

ItemVendaFormSet = forms.inlineformset_factory(
    Venda, ItemVenda,
    fields=['tipo_item', 'quantidade', 'preco_unitario'],
    extra=1, # Começa com apenas 1 linha
    can_delete=True
)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')
        labels = {
            "username": "Nome de usuário",
            "email": "E-mail",
        }


class CustomUserCreationForm(UserCreationForm):

    TIPO_USER_CHOICES = [
        ('FUNC', 'Funcionário'),
        ('ADMIN', 'Administrador'),
    ]
    tipo_usuario = forms.ChoiceField(
        choices= TIPO_USER_CHOICES,
        label = "Nível de acesso",
        initial = 'FUNC',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    password1 = forms.CharField(
        label='Senha', strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text="A senha deve ter no mínimo 8 caracteres.")

    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text="Digite a senha novamente para confirmar."
    )

    class Meta:
        model = User
        fields = ("username", "email")
        labels = {
            "username": "Nome de usuário",
            "email": "E-mail",
        }
        help_texts = {
            "username": "Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas.",
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        tipo = self.cleaned_data.get('tipo_usuario')

        if tipo == 'ADMIN':
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False
            user.is_staff = False

        if commit:
            user.save()
        return user