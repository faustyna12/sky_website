from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class ReportsDashboardTest(TestCase):

    def setUp(self):
        # Create a normal user
        self.normal_user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpass123'
        )
        self.client = Client()

    def test_normal_user_cannot_access_reports(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('reports_dashboard'))
        self.assertNotEqual(response.status_code, 200)

    def test_admin_can_access_reports(self):
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(reverse('reports_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_reports_shows_correct_user_count(self):
        self.client.login(username='adminuser', password='adminpass123')
        response = self.client.get(reverse('reports_dashboard'))
        self.assertContains(response, '2')

    def test_logged_out_user_cannot_access_reports(self):
        response = self.client.get(reverse('reports_dashboard'))
        self.assertNotEqual(response.status_code, 200)
