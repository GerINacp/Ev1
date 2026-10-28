from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from Tours.models import Reserva, UserProfile, Viajes

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'journey-input',
            'placeholder': 'Crea una contraseña',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'journey-input',
            'placeholder': 'Repite la contraseña',
        })
        for field_name, field in self.fields.items():
            if field_name not in {'password1', 'password2'}:
                field.widget.attrs.update({
                    'class': 'journey-input',
                    'placeholder': f'Ingresa {field.label.lower()}',
                })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'rol': 'cliente'}
            )
        return user


class AccesoForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'journey-input',
            'placeholder': 'Tu usuario',
            'autocomplete': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'journey-input',
            'placeholder': 'Tu contraseña',
            'autocomplete': 'current-password',
        })


class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = [
            'nombre_cliente',
            'email',
            'telefono',
            'tour',
            'fecha_reserva',
            'cantidad_personas',
        ]
        widgets = {
            'fecha_reserva': forms.DateInput(attrs={'type': 'date'}),
            'cantidad_personas': forms.NumberInput(attrs={'min': 1, 'max': 30}),
            'telefono': forms.TextInput(attrs={'type': 'tel', 'autocomplete': 'tel'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'journey-input'
        self.fields['fecha_reserva'].widget.attrs['min'] = timezone.localdate().isoformat()

    def clean_fecha_reserva(self):
        fecha = self.cleaned_data['fecha_reserva']
        if fecha < timezone.localdate():
            raise forms.ValidationError('Elige una fecha de hoy en adelante.')
        return fecha


class TourAdminForm(forms.ModelForm):
    class Meta:
        model = Viajes
        fields = ['nombre', 'descripcion', 'precio', 'imagen']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'precio': forms.NumberInput(attrs={'min': 0, 'step': 1000}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'journey-input'