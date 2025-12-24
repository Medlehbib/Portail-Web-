from django import forms
from .models import Article, Annonce
from django.contrib.auth.models import User
from .models import CommandeAnnonce



class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image', 'video', 'categorie']

class AnnonceForm(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ['titre', 'description', 'image', 'prix']

class AdminCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.is_staff = True          # Admin
        user.is_superuser = False     # ليس Super Admin
        if commit:
            user.save()
        return user

# class CommandeAnnonceForm(forms.ModelForm):
#     class Meta:
#         model = CommandeAnnonce
#         fields = ['nom', 'email', 'annonce', 'message']
#         widgets = {
#             'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Votre message...'}),
#             'nom': forms.TextInput(attrs={'placeholder': 'Votre nom'}),
#             'email': forms.EmailInput(attrs={'placeholder': 'Votre email'}),
#         }
#


class CommanderAnnonceForm(forms.Form):
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 4,
            "placeholder": "Décrivez votre commande ici..."
        })
    )
    email = forms.EmailField(
        label="Votre Email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "exemple@mail.com"
        })
    )

class CommanderAnnonceForm(forms.ModelForm):
    class Meta:
        model = CommandeAnnonce
        fields = ['nom', 'email', 'message']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre nom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Votre email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Votre message'}),
        }