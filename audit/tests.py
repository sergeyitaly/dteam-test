from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import RequestLog

class RequestLoggingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_request_logging(self):
        # Test anonymous request
        response = self.client.get('/')
        log = RequestLog.objects.first()
        self.assertEqual(log.method, 'GET')
        self.assertEqual(log.path, '/')
        self.assertEqual(log.user, None)

        # Test authenticated request
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/')
        log = RequestLog.objects.filter(user=self.user).first()
        self.assertEqual(log.user, self.user)

    def test_logs_view(self):
        RequestLog.objects.create(
            method='GET',
            path='/test/',
            response_code=200
        )
        response = self.client.get('/logs/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/test/')