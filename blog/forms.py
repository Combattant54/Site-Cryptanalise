from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField(label="Votre addresse mail")
    sendback = forms.BooleanField(required=False, help_text="Recevez une copie du mail envoyé")

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Votre nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Votre mot de passe", widget=forms.PasswordInput)