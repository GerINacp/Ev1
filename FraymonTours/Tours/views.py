from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Vista de Registro
def registro_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'Tours/registro.html', {'form': form})

# Vista Principal (Protegida)
@login_required(login_url='login')
def index_view(request):
    return render(request, 'Tours/index.html')