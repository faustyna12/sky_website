from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Department, TeamType, Team

class OrganisationTests(TestCase):
    def setUp(self):
        # 1. Setup User
        self.user = User.objects.create_user(username='sky_tester', password='password123')
        
        # 2. Setup Metadata
        self.dept_data = Department.objects.create(name="Data Engineering")
        self.dept_it = Department.objects.create(name="IT Support")
        self.type_backend = TeamType.objects.create(name="Backend")
        self.type_frontend = TeamType.objects.create(name="Frontend")

        # 3. Setup Teams
        self.team_alpha = Team.objects.create(
            name="Alpha Team",
            department=self.dept_data,
            team_type=self.type_backend,
            members_count=5,
            specialization="Python"
        )
        self.team_beta = Team.objects.create(
            name="Beta Team",
            department=self.dept_it,
            team_type=self.type_frontend,
            members_count=3,
            specialization="React"
        )
        self.client = Client()

    # --- ACCESS CONTROL ---
    def test_org_map_view_requires_login(self):
        """Test 1: Ensure the page redirects to login if not authenticated"""
        response = self.client.get(reverse('org_map'))
        self.assertEqual(response.status_code, 302)

    def test_view_accessible_after_login(self):
        """Test 2: Ensure logged-in users can reach the page"""
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('org_map'))
        self.assertEqual(response.status_code, 200)

    # --- FILTERING LOGIC ---
    def test_team_type_filter_working(self):
        """Test 3: Filter by team_type (Matches request.GET.get('team_type'))"""
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('org_map'), {'team_type': self.type_frontend.id})
        self.assertContains(response, "Beta Team")
        self.assertNotContains(response, "Alpha Team")

    def test_department_filter_working(self):
        """Test 4: Filter by department"""
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('org_map'), {'department': self.dept_data.id})
        self.assertContains(response, "Alpha Team")
        self.assertNotContains(response, "Beta Team")

    def test_reset_filters_default(self):
        """Test 5: Sending 'all' returns all records (Simulation of Reset)"""
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('org_map'), {'department': 'all', 'team_type': 'all'})
        self.assertContains(response, "Alpha Team")
        self.assertContains(response, "Beta Team")

    # --- UI & TEMPLATE CONTENT ---
    def test_department_clickable_and_popup(self):
        """Test 6: Verify the openModal trigger exists in HTML"""
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('org_map'))
        self.assertContains(response, f"openModal('{self.dept_data.name}'")

    def test_context_data_counts(self):
        """Test 7: Verify 'total_teams' context variable is accurate"""
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('org_map'))
        self.assertEqual(response.context['total_teams'], 2)

    def test_team_detail_links_present(self):
        """Test 8: Verify individual team links exist in the map"""
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('org_map'))
        self.assertContains(response, f'href="/teams/{self.team_alpha.id}/"')

    # --- CSV EXPORT ---
    def test_csv_export_status(self):
        """Test 9: Ensure CSV export endpoint is healthy"""
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('export_teams_csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_csv_export_content(self):
        """Test 10: Check if specific team data is inside the generated CSV"""
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('export_teams_csv'))
        content = response.content.decode('utf-8')
        self.assertIn("Alpha Team", content)
        self.assertIn("Python", content)

    # --- DATA INTEGRITY ---
    def test_empty_departments_not_shown(self):
        """Test 11: Departments with no teams should not appear in display_departments"""
        # Create a new department with no teams
        empty_dept = Department.objects.create(name="Empty Dept")
        self.client.login(username='sky_tester', password='password123')
        response = self.client.get(reverse('org_map'))
        # It should be in the filter dropdown (departments_list)
        self.assertIn(empty_dept, response.context['departments_list'])
        # But NOT in the display (departments) because it has no teams
        self.assertNotIn(empty_dept, response.context['departments'])