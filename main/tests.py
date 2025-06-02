from rest_framework.test import APITestCase
from .models import CV

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