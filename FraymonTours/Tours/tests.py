from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from Tours.models import Reserva


class AccountAndQuoteFlowTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='traveler_test',
			password='TripPassword!482',
			email='traveler@example.com',
		)

	def test_login_authenticates_and_returns_to_landing(self):
		response = self.client.post(reverse('login'), {
			'username': 'traveler_test',
			'password': 'TripPassword!482',
		})

		self.assertRedirects(response, reverse('landing'))
		self.assertIn('_auth_user_id', self.client.session)

	def test_login_shows_error_for_invalid_credentials(self):
		response = self.client.post(reverse('login'), {
			'username': 'traveler_test',
			'password': 'wrong-password',
		})

		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.context['form'].non_field_errors())

	def test_registration_creates_and_authenticates_user(self):
		response = self.client.post(reverse('registro'), {
			'username': 'new_traveler',
			'email': 'new@example.com',
			'password1': 'JourneyPassword!482',
			'password2': 'JourneyPassword!482',
		})

		self.assertRedirects(response, reverse('landing'))
		self.assertTrue(User.objects.filter(username='new_traveler').exists())
		self.assertIn('_auth_user_id', self.client.session)

	def test_quote_form_prefills_selected_tour(self):
		response = self.client.get(reverse('cotizar'), {'tour': 'vina_del_mar'})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context['form']['tour'].value(), 'vina_del_mar')

	def test_quote_request_is_saved(self):
		response = self.client.post(reverse('cotizar'), {
			'nombre_cliente': 'Persona de prueba',
			'email': 'quote@example.com',
			'telefono': '+56912345678',
			'tour': 'vina_del_mar',
			'fecha_reserva': (date.today() + timedelta(days=30)).isoformat(),
			'cantidad_personas': 2,
		}, follow=True)

		self.assertEqual(response.status_code, 200)
		self.assertIn((reverse('cotizar'), 302), response.redirect_chain)
		self.assertContains(response, 'Solicitud recibida')
		self.assertEqual(Reserva.objects.count(), 1)
