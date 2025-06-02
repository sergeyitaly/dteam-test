from rest_framework.test import APITestCase
from .models import CV
from django.test import TestCase, RequestFactory
from .context_processors import settings_context
from django.contrib.auth.models import User

class SettingsContextTests(TestCase):
    def test_context_processor(self):
        request = RequestFactory().get('/')
        context = settings_context(request)
        self.assertIn('settings', context)
        self.assertIn('DEBUG', context['settings'])

class SettingsViewTests(TestCase):
    def setUp(self):
        # Create a staff user for testing
        self.staff_user = User.objects.create_user(
            username='staff',
            password='password',
            is_staff=True
        )
        # Create regular user
        self.regular_user = User.objects.create_user(
            username='regular',
            password='password'
        )

    def test_settings_view_as_staff(self):
        self.client.login(username='staff', password='password')
        response = self.client.get('/settings/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DEBUG')
        self.assertContains(response, 'INSTALLED_APPS')

    def test_settings_view_as_anonymous(self):
        response = self.client.get('/settings/')
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_settings_view_as_regular_user(self):
        self.client.login(username='regular', password='password')
        response = self.client.get('/settings/')
        # Regular users should be denied access (403 Forbidden)
        self.assertEqual(response.status_code, 403)

class CVAPITestCase(APITestCase):
    def setUp(self):
        self.cv = CV.objects.create(
            first_name="Test",
            last_name="User",
            bio="API Test",
            contacts={"email": "test@api.com"}
        )

    def test_cv_list(self):
        response = self.client.get('/api/cvs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_cv_detail(self):
        response = self.client.get(f'/api/cvs/{self.cv.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'Test')

    def test_cv_create(self):
        data = {
            "first_name": "New",
            "last_name": "CV",
            "bio": "Created via API",
            "contacts": {"email": "new@cv.com"}
        }
        response = self.client.post('/api/cvs/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(CV.objects.count(), 2)

    def test_cv_update(self):
        data = {"first_name": "Updated"}
        response = self.client.patch(f'/api/cvs/{self.cv.id}/', data, format='json')
        self.assertEqual(response.status_code, 200)
        self.cv.refresh_from_db()
        self.assertEqual(self.cv.first_name, 'Updated')

    def test_cv_delete(self):
        response = self.client.delete(f'/api/cvs/{self.cv.id}/')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(CV.objects.count(), 0)