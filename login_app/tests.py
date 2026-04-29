from django.test import TestCase, Client
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User

class LoginAppTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # URL Logic
        try:
            self.login_url = reverse('login')
        except NoReverseMatch:
            self.login_url = '/login/'

        # FIXED: Your app redirects to /dashboard/, so we set this accordingly
        try:
            # If you have a named URL for dashboard, use it, otherwise use the path
            self.dashboard_url = '/dashboard/' 
        except NoReverseMatch:
            self.dashboard_url = '/dashboard/'

        self.test_user = User.objects.create_user(
            username='rafia_admin', 
            password='admin',
            email='rafia@sky.uk'
        )

    # --- AUTHENTICATION FLOWS ---
    def test_login_page_loads(self):
        """Test 1: Verify login page renders with OpenSky branding"""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "OpenSky")

    def test_successful_login_redirect(self):
        """Test 2: Valid credentials redirect to the dashboard"""
        response = self.client.post(self.login_url, {
            'username': 'rafia_admin',
            'password': 'admin'
        })
        # This will now match the '/dashboard/' redirect seen in your logs
        self.assertRedirects(response, self.dashboard_url)

    def test_invalid_login_denied(self):
        """Test 3: Incorrect login does not create a session"""
        response = self.client.post(self.login_url, {
            'username': 'sky_pilot',
            'password': 'wrongpassword'
        })
        self.assertFalse('_auth_user_id' in self.client.session)

    # --- UI & SECURITY ---
    def test_login_csrf_protection(self):
        """Test 4: Verify CSRF token is present in the form"""
        response = self.client.get(self.login_url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_password_field_is_hidden(self):
        """Test 5: Verify password input type is security-masked"""
        response = self.client.get(self.login_url)
        self.assertContains(response, 'type="password"')

    def test_remember_me_checkbox_exists(self):
        """Test 6: Verify 'Remember' checkbox is present"""
        response = self.client.get(self.login_url)
        self.assertContains(response, 'Remember')
        self.assertContains(response, 'type="checkbox"')

    def test_forgot_password_link_exists(self):
        """Test 7: Verify 'Forgot?' link is present"""
        response = self.client.get(self.login_url)
        self.assertContains(response, 'Forgot?')

    # --- FORGOT PASSWORD PAGE ---
    def test_forgot_password_page_content(self):
        """Test 8: Verify the Security Protocol message on reset page"""
        try:
            url = reverse('forgot_password')
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Security Protocol")
        except NoReverseMatch:
            # Fallback if URL name is different
            response = self.client.get('/forgot-password/')
            self.assertEqual(response.status_code, 200)

    # --- EDGE CASES ---
    def test_admin_login_link_present(self):
        """Test 9: Verify the shortcut to Admin Login exists"""
        response = self.client.get(self.login_url)
        self.assertContains(response, "Admin Login")

    def test_inactive_user_login(self):
        """Test 10: Disabled accounts cannot log in"""
        self.test_user.is_active = False
        self.test_user.save()
        response = self.client.post(self.login_url, {
            'username': 'rafia_admin',
            'password': 'admin'
        })
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_empty_login_fields(self):
        """Test 11: Empty submission fails"""
        response = self.client.post(self.login_url, {'username': '', 'password': ''})
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_branding_footer(self):
        """Test 12: Verify the 2026 Copyright notice"""
        response = self.client.get(self.login_url)
        self.assertContains(response, "© 2026 Open Sky Aviation Group")

    def test_utility_bar_links(self):
        """Test 13: Verify Help and Contact Support links"""
        response = self.client.get(self.login_url)
        self.assertContains(response, "Help")
        self.assertContains(response, "ContactSupport")

    def test_email_label_styling(self):
        """Test 14: Verify UI labels (matches actual HTML text)"""
        response = self.client.get(self.login_url)
        # FIXED: Look for "Email Address" as it appears in your HTML source
        self.assertContains(response, "Email Address")
        self.assertContains(response, "Password")

    