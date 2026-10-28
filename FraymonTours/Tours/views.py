from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from Tours.forms import AccesoForm, CotizacionForm, RegistroForm
from Tours.models import Viajes


def _safe_next_url(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None

def landing_view(request):
    tours = Viajes.objects.all()
    return render(request, 'Tours/landing.html', {'tours': tours})

def legacy_index_redirect(request):
    return redirect('landing')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('landing')

    form = AccesoForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        auth_login(request, form.get_user())
        return redirect(_safe_next_url(request) or 'landing')

    return render(request, 'login.html', {
        'form': form,
        'next': _safe_next_url(request),
    })


@require_POST
def logout_view(request):
    auth_logout(request)
    return redirect('landing')

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('landing')

    tours = Viajes.objects.all()
    form = RegistroForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        auth_login(request, user)
        return redirect(_safe_next_url(request) or 'landing')

    return render(request, 'Tours/registro.html', {
        'form': form,
        'next': _safe_next_url(request),
        'tours': tours,
    })


def cotizar_view(request):
    initial = {'tour': request.GET.get('tour', '')}
    if request.user.is_authenticated:
        initial.update({
            'nombre_cliente': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        })
    form = CotizacionForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        reserva = form.save()
        messages.success(
            request,
            f'Recibimos tu solicitud para {reserva.get_tour_display()}. El equipo de Fraymon Tours podrá contactarte con los detalles.',
        )
        return redirect('cotizar')

    return render(request, 'Tours/cotizar.html', {'form': form})