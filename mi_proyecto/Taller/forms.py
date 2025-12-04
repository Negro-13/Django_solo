from django import forms

class FormularioMatricula(forms.Form):
    matricula = forms.IntegerField(label="Cliente")
    nombre = forms.CharField(label="Nombre y Apellido", max_length=45)

class LoginForm(forms.Form):
    usuario = forms.CharField(
        max_length=50,
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    clave = forms.CharField(
        max_length=50,
        label="Clave",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

class RegistroForm(forms.Form):
    usuario = forms.CharField(
        max_length=50,
        label="Usuario",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    clave = forms.CharField(
        max_length=50,
        label="Clave",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

class ClienteForm(forms.Form):
    dni = forms.CharField(max_length=20)
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    direccion = forms.CharField(max_length=100)
    telefono = forms.CharField(max_length=20)

class VehiculoForm(forms.Form):
    patente = forms.CharField(max_length=20)
    dni = forms.CharField(max_length=20)
    marca = forms.CharField(max_length=50)
    modelo = forms.CharField(max_length=50)
    color = forms.CharField(max_length=30)
