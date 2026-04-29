from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from organisation_app.models import Team, Department

class SkyDashTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # 1. Create a Department first (Required to avoid IntegrityError)
        self.dept = Department.objects.create(name="Operations")
        
        # 2. Create the Team and link it to the Department
        self.team = Team.objects.create(
            name="Flight Ops",
            department=self.dept  # This satisfies the NOT NULL constraint
        )
        
        # 3. Create a test user
        self.user = User.objects.create_user(
            username='rafia_admin', 
            password='admin',
            first_name='Rafia',
            last_name='Admin',
            email='rafia@sky.uk'
        )
        
        # URL mapping
        self.dash_url = reverse('dashboard_home')
        self.profile_url = reverse('user_profile')

    # ... keep the rest of your tests the same ...

    # --- DASHBOARD AUTHENTICATION TESTS ---
    
    def test_dashboard_status_code(self):
        """Test 1: Dashboard loads successfully for any visitor"""
        response = self.client.get(self.dash_url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_welcome_authenticated(self):
        """Test 2: Dashboard displays user's first name if logged in"""
        self.client.login(username='rafia_admin', password='admin')
        response = self.client.get(self.dash_url)
        self.assertContains(response, "Welcome, Rafia!")

    def test_dashboard_welcome_guest(self):
        """Test 3: Dashboard defaults to 'Guest' for unauthenticated users"""
        response = self.client.get(self.dash_url)
        self.assertContains(response, "Welcome, Guest!")

    # --- DASHBOARD UI & CONTENT ---

    def test_dashboard_directory_text(self):
        """Test 4: Verify directory tagline exists"""
        response = self.client.get(self.dash_url)
        self.assertContains(response, "Access the Sky Streaming Organisation Directory")

    def test_search_placeholder_present(self):
        """Test 5: Verify the search bar exists with correct placeholder"""
        response = self.client.get(self.dash_url)
        self.assertContains(response, "Search teams, departments, or managers...")

    def test_action_card_teams(self):
        """Test 6: Verify 'Find a Team' action card is rendered"""
        response = self.client.get(self.dash_url)
        self.assertContains(response, "Find a Team")

    def test_action_card_map(self):
        """Test 7: Verify 'View Map' action card is rendered"""
        response = self.client.get(self.dash_url)
        self.assertContains(response, "View Map")

    def test_action_card_messages(self):
        """Test 8: Verify 'Contact Teams' action card is rendered"""
        response = self.client.get(self.dash_url)
        self.assertContains(response, "Contact Teams")

    def test_recent_activity_empty_state(self):
        """Test 9: Verify empty state message for system logs"""
        response = self.client.get(self.dash_url)
        self.assertContains(response, "No recent system logs")

    def test_dashboard_uses_correct_template(self):
        """Test 10: Verify dashboard uses the specific sky_dash template"""
        response = self.client.get(self.dash_url)
        self.assertTemplateUsed(response, 'sky_dash/sky_dash.html')

    # --- USER PROFILE TESTS ---

    def test_profile_redirects_unauthenticated(self):
        """Test 11: Profile access is restricted via @login_required"""
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 302)

    def test_profile_loads_authenticated(self):
        """Test 12: Authenticated user can view profile"""
        self.client.login(username='rafia_admin', password='admin')
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, 200)

    def test_profile_displays_full_name(self):
        """Test 13: Profile shows combined First and Last name"""
        self.client.login(username='rafia_admin', password='admin')
        response = self.client.get(self.profile_url)
        self.assertContains(response, "Rafia Admin")

    def test_profile_displays_email(self):
        """Test 14: Profile shows the user email"""
        self.client.login(username='rafia_admin', password='admin')
        response = self.client.get(self.profile_url)
        self.assertContains(response, "rafia@sky.uk")

    def test_profile_avatar_integration(self):
        """Test 15: Verify the UI-Avatars API link is generated correctly"""
        self.client.login(username='rafia_admin', password='admin')
        response = self.client.get(self.profile_url)
        self.assertContains(response, "ui-avatars.com/api/?name=rafia")

    def test_profile_back_link(self):
        """Test 16: Verify the link back to the dashboard exists"""
        self.client.login(username='rafia_admin', password='admin')
        response = self.client.get(self.profile_url)
        self.assertContains(response, "Back To Dashboard")

    # --- VIEW CONTEXT DATA ---

    def test_dashboard_context_team_count(self):
        """Test 17: Verify total_teams_count is passed in context"""
        response = self.client.get(self.dash_url)
        self.assertEqual(response.context['total_teams_count'], 1)

    def test_dashboard_recent_teams_ordering(self):
        """Test 18: Verify recent_teams context contains the created team"""
        response = self.client.get(self.dash_url)
        self.assertIn(self.team, response.context['recent_teams'])