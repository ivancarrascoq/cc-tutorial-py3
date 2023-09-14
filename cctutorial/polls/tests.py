from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class PollsTests(TestCase):
    """
    Simple tests for the polls app
    """

    def test_choices(self):
        """Test the choices view"""

        response = self.client.get(reverse('choices'))
        self.assertEqual(response.status_code, 200)

        # Add a test for a non-existant ID and test for the expected result

    def test_most_popular_choice(self):

        response = self.client.get(reverse('most-popular-choice'))
        self.assertEqual(response.status_code, 200)
