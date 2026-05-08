from django.test import TestCase
from django.urls import reverse

class SignUpPageTests(TestCase):
    def test_signup_url_by_name(self):
        # We expect a URL named 'signup' to exist and return 200 OK
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_signup_uses_correct_template(self):
        # We expect it to use a specific HTML file
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'registration/signup.html')
