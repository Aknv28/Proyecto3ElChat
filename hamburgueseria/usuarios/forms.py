from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from datetime import date
from .models import Usuario


class UsuarioCreationForm(UserCreationForm):
    # Campos personalizados con validaciones y mensajes en español
    first_name = forms.CharField(
        label='Nombres',
        max_length=50,
        required=True,
        error_messages={
            'required': 'El nombre es requerido',
            'max_length': 'El nombre no puede exceder 50 caracteres',
        }
    )

    last_name = forms.CharField(
        label='Apellidos',
        max_length=50,
        required=True,
        error_messages={
            'required': 'El apellido es requerido',
            'max_length': 'El apellido no puede exceder 50 caracteres',
        }
    )

    email = forms.EmailField(
        label='Correo Electrónico',
        required=True,
        error_messages={
            'required': 'El correo electrónico es requerido',
            'invalid': 'Ingresa un correo electrónico válido',
        }
    )

    carnet_numero = forms.CharField(
        label='Número de Carnet',
        max_length=10,
        required=True,
        error_messages={
            'required': 'El número de carnet es requerido',
            'max_length': 'El carnet no debe exceder 10 dígitos',
        }
    )

    carnet_complemento = forms.CharField(
        label='Complemento (Opcional)',
        max_length=3,
        required=False,
    )

    fecha_nacimiento = forms.DateField(
        label='Fecha de Nacimiento',
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        error_messages={
            'required': 'La fecha de nacimiento es requerida',
            'invalid': 'Ingresa una fecha válida',
        }
    )

    telefono = forms.CharField(
        label='Teléfono',
        max_length=15,
        required=True,
        error_messages={
            'required': 'El teléfono es requerido',
            'max_length': 'El teléfono no debe exceder 15 caracteres',
        }
    )

    direccion = forms.CharField(
        label='Dirección',
        max_length=200,
        required=True,
        widget=forms.Textarea(attrs={'rows': 2}),
        error_messages={
            'required': 'La dirección es requerida',
            'max_length': 'La dirección no debe exceder 200 caracteres',
        }
    )

    rol = forms.ChoiceField(
        label='Rol',
        choices=[
            ('', 'Selecciona un rol'),
            ('admin', 'Administrador'),
            ('cajero', 'Cajero'),
            ('cocinero', 'Cocinero'),
        ],
        required=True,
        error_messages={
            'required': 'Debes seleccionar un rol',
        }
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=20,
        error_messages={
            'required': 'La contraseña es requerida',
            'min_length': 'La contraseña debe tener al menos 8 caracteres',
            'max_length': 'La contraseña no debe exceder 20 caracteres',
        }
    )

    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput,
        min_length=8,
        max_length=20,
        error_messages={
            'required': 'Debes confirmar la contraseña',
        }
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email', 'rol',
            'fecha_nacimiento', 'telefono', 'direccion', 'password1', 'password2'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # El campo username estará oculto (autogenerado)
        self.fields['username'].required = False
        self.fields['username'].widget = forms.HiddenInput()

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Las contraseñas no coinciden')

        return password2

    def clean_fecha_nacimiento(self):
        fecha_nac = self.cleaned_data.get('fecha_nacimiento')

        if fecha_nac:
            today = date.today()
            age = today.year - fecha_nac.year - ((today.month, today.day) < (fecha_nac.month, fecha_nac.day))

            if fecha_nac > today:
                raise ValidationError('No puedes ingresar una fecha futura')

            if age < 18:
                raise ValidationError(f'Debes ser mayor de 18 años (edad actual: {age} años)')

            if age > 100:
                raise ValidationError('La fecha ingresada no es válida')

        return fecha_nac

    def clean_carnet_numero(self):
        carnet = self.cleaned_data.get('carnet_numero')

        if carnet:
            if not carnet.isdigit():
                raise ValidationError('El carnet solo debe contener números')

            if len(carnet) < 6:
                raise ValidationError('El carnet debe tener al menos 6 dígitos')

        return carnet

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        if telefono:
            telefono_limpio = telefono.replace(' ', '').replace('-', '').replace('+', '')
            if len(telefono_limpio) < 7:
                raise ValidationError('El teléfono debe tener al menos 7 dígitos')

        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')

        if direccion and len(direccion.strip()) < 10:
            raise ValidationError('La dirección debe tener al menos 10 caracteres')

        return direccion

    def clean(self):
        cleaned_data = super().clean()

        # Generar username automáticamente
        carnet_numero = cleaned_data.get('carnet_numero')
        carnet_complemento = cleaned_data.get('carnet_complemento', '').strip().lower()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if carnet_numero and first_name and last_name:
            username = carnet_numero
            if carnet_complemento:
                username += '-' + carnet_complemento
            username += '-' + first_name[0].lower() + last_name[0].lower()
            cleaned_data['username'] = username

            # Verificar si el username ya existe
            if Usuario.objects.filter(username=username).exists():
                raise ValidationError(f'Ya existe un usuario con este carnet y nombre: {username}')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Combinar carnet_numero + carnet_complemento en un solo campo "carnet"
        carnet_numero = self.cleaned_data.get('carnet_numero', '').strip()
        carnet_complemento = self.cleaned_data.get('carnet_complemento', '').strip().upper()

        if carnet_complemento:
            user.carnet = f"{carnet_numero}-{carnet_complemento}"
        else:
            user.carnet = carnet_numero

        if commit:
            user.save()

        return user


class UsuarioChangeForm(UserChangeForm):
    first_name = forms.CharField(
        label='Nombres',
        max_length=50,
        required=True,
        error_messages={
            'required': 'El nombre es requerido',
            'max_length': 'El nombre no puede exceder 50 caracteres',
        }
    )

    last_name = forms.CharField(
        label='Apellidos',
        max_length=50,
        required=True,
        error_messages={
            'required': 'El apellido es requerido',
            'max_length': 'El apellido no puede exceder 50 caracteres',
        }
    )

    email = forms.EmailField(
        label='Correo Electrónico',
        required=True,
        error_messages={
            'required': 'El correo electrónico es requerido',
            'invalid': 'Ingresa un correo electrónico válido',
        }
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name', 'email', 'rol',
            'carnet', 'fecha_nacimiento', 'telefono', 'direccion'
        ]
