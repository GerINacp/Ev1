from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from Tours.models import Reserva

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'journey-input',
                'placeholder': f'Ingresa {field.label.lower()}',
            })


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