from django.test import SimpleTestCase


class DashboardTests(SimpleTestCase):
    def test_dashboard_shows_json_data(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nebula")
        self.assertContains(response, "FastAPI")
        self.assertContains(response, "Java &amp; Database Engineering")
