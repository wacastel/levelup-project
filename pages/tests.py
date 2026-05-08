from django.test import SimpleTestCase
from django.urls import reverse

class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        # We expect the root URL to return a 200 status code
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # New assertion: check that 'home.html' is the template used
        self.assertTemplateUsed(response, "home.html")

    def test_homepage_contains_correct_html(self):
        # We expect the content to say "Hello, World!"
        response = self.client.get("/")
        self.assertContains(response, "Welcome to LevelUp")
