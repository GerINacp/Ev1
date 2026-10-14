from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistroForm


# Create your views here.
def inicio(request):
    return render(request, 'Tours/index.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Cuenta creada con éxito para {username}! Ya puedes iniciar sesión.')
            return redirect('index')  # Te redirige a la página principal
    else:
        form = RegistroForm()
    
    return render(request, 'Tours/registro.html', {'form': form})