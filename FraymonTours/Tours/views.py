from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from Tours.forms import AccesoForm, CotizacionForm, RegistroForm, TourAdminForm
from Tours.models import Empleado, Reserva, UserProfile, Viajes


def _safe_next_url(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return next_url
    return None


def _get_profile_or_default(user):
    try:
        return user.profile
    except UserProfile.DoesNotExist:
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'rol': 'cliente'},
        )
        return profile


def _redirect_by_role(user):
    profile = _get_profile_or_default(user)

    if profile.rol == 'empleado':
        return 'empleado_dashboard'
    if profile.rol == 'admin':
        return 'admin_dashboard'
    return 'landing'


@login_required
def empleado_dashboard(request):
    profile = _get_profile_or_default(request.user)
    if profile.rol != 'empleado':
        return redirect('landing')

    reservas = Reserva.objects.order_by('fecha_reserva', 'creado_el')
    rutas = Viajes.objects.order_by('nombre')
    perfil = Empleado.objects.filter(user=request.user).first()

    return render(request, 'Tours/empleado_dashboard.html', {
        'reservas': reservas,
        'rutas': rutas,
        'perfil': perfil,
        'usuario': request.user,
    })


def landing_view(request):
    tours = Viajes.objects.all()
    return render(request, 'Tours/landing.html', {'tours': tours})


def legacy_index_redirect(request):
    return redirect('landing')


def login_view(request):
    if request.user.is_authenticated:
        return redirect(_redirect_by_role(request.user))

    form = AccesoForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        auth_login(request, form.get_user())
        return redirect(_safe_next_url(request) or _redirect_by_role(request.user))

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
        return redirect(_safe_next_url(request) or _redirect_by_role(user))

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


@login_required
def cambiar_estado_reserva(request, reserva_id):
    profile = _get_profile_or_default(request.user)
    if profile.rol != 'empleado':
        return redirect('landing')

    reserva = Reserva.objects.get(id=reserva_id)
    nuevo_estado = request.POST.get('estado')
    if nuevo_estado in dict(Reserva.ESTADO_CHOICES):
        reserva.estado = nuevo_estado
        reserva.save()
        messages.success(request, f'Estado de la reserva de {reserva.nombre_cliente} actualizado.')
    return redirect('empleado_dashboard')


@login_required
def empleado_perfil(request):
    profile = _get_profile_or_default(request.user)
    if profile.rol != 'empleado':
        return redirect('landing')

    perfil = Empleado.objects.filter(user=request.user).first()
    return render(request, 'Tours/empleado_perfil.html', {'perfil': perfil})


@login_required
def admin_dashboard(request):
    profile = _get_profile_or_default(request.user)
    if profile.rol != 'admin':
        return redirect('landing')

    reservas = Reserva.objects.order_by('fecha_reserva', 'creado_el')
    rutas = Viajes.objects.order_by('nombre')

    return render(request, 'Tours/admin_dashboard.html', {
        'reservas': reservas,
        'rutas': rutas,
        'usuario': request.user,
    })


@login_required
def admin_tours(request):
    profile = _get_profile_or_default(request.user)
    if profile.rol != 'admin':
        return redirect('landing')

    tours = Viajes.objects.order_by('nombre')
    if request.method == 'POST':
        form = TourAdminForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tour actualizado correctamente.')
            return redirect('admin_tours')
    else:
        form = TourAdminForm()

    return render(request, 'Tours/admin_tours.html', {
        'tours': tours,
        'form': form,
        'usuario': request.user,
    })


@login_required
def admin_editar_tour(request, tour_id):
    profile = _get_profile_or_default(request.user)
    if profile.rol != 'admin':
        return redirect('landing')

    tour = Viajes.objects.get(pk=tour_id)
    if request.method == 'POST':
        form = TourAdminForm(request.POST, request.FILES, instance=tour)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tour {tour.nombre} actualizado correctamente.')
            return redirect('admin_tours')
    else:
        form = TourAdminForm(instance=tour)

    return render(request, 'Tours/admin_editar_tour.html', {
        'form': form,
        'tour': tour,
        'usuario': request.user,
    })


@login_required
def admin_editar_reserva(request, reserva_id):
    profile = _get_profile_or_default(request.user)
    if profile.rol != 'admin':
        return redirect('landing')

    reserva = Reserva.objects.get(pk=reserva_id)
    precio_lookup = {
        'vina_del_mar': ['Viña del Mar', 'Viña', 'vina'],
        'farellones': ['Farellones', 'Valle Nevado', 'Farellones & Valle Nevado'],
        'city_tour': ['City Tour', 'city', 'tour'],
    }
    keywords = precio_lookup.get(reserva.tour, [reserva.get_tour_display()])
    tour = None
    for keyword in keywords:
        tour = Viajes.objects.filter(nombre__icontains=keyword).first()
        if tour:
            break

    precio_base = 0
    if tour and tour.precio:
        precio_base = int(tour.precio)
    elif reserva.tour == 'vina_del_mar':
        precio_base = 79000
    elif reserva.tour == 'farellones':
        precio_base = 129000
    elif reserva.tour == 'city_tour':
        precio_base = 45000

    precio_total = precio_base * reserva.cantidad_personas

    if request.method == 'POST':
        nueva_fecha = request.POST.get('fecha_reserva')
        nuevas_personas = request.POST.get('cantidad_personas')
        nuevo_estado = request.POST.get('estado')

        if nueva_fecha:
            reserva.fecha_reserva = nueva_fecha
        if nuevas_personas:
            reserva.cantidad_personas = int(nuevas_personas)
        if nuevo_estado in dict(Reserva.ESTADO_CHOICES):
            reserva.estado = nuevo_estado

        reserva.save()
        messages.success(request, f'Reserva de {reserva.nombre_cliente} actualizada correctamente.')
        return redirect('admin_dashboard')

    return render(request, 'Tours/admin_editar_reserva.html', {
        'reserva': reserva,
        'usuario': request.user,
        'precio_base': precio_base,
        'precio_total': precio_total,
    })