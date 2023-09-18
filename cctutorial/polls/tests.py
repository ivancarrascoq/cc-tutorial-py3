from django.test import TestCase
from django.urls import reverse
from .models import Choice, Question
from django.utils import timezone
from datetime import timedelta


# Create your tests here.
class PollsTests(TestCase):
    """
    Simple tests for the polls app
    """

    def setUp(self):
        self.question = Question.objects.create(
            id=100,
            question_text="Question 1",
            pub_date=timezone.make_aware(timezone.datetime(2023, 9, 16)),
        )
        self.choice1 = Choice.objects.create(
            id=200,
            choice_text="Choice 1",
            votes=0,
            question_id=100,
        )
        self.choice2 = Choice.objects.create(
            id=201,
            choice_text="Choice 2",
            votes=0,
            question_id=100,
        )

    def test_choices(self):
        """Test the choices view"""

        response = self.client.get(reverse("polls:choices"))
        self.assertEqual(response.status_code, 200)

        # Add a test for a non-existant ID and test for the expected result

    def test_choices_pk(self):
        """Test the choice view with a pk"""

        response = self.client.get(reverse("polls:choices", args=("0200",)))
        self.assertEqual(response.status_code, 200)

    def test_choices_pk_does_not_exist(self):
        """Test the choice view with a pk"""

        response = self.client.get(reverse("polls:choices", args=("0300",)))
        self.assertEqual(response.status_code, 404)

    def test_most_popular_choice(self):
        """Test the most popular choice view"""

        response = self.client.get(reverse("polls:most-popular-choice"))
        self.assertEqual(response.status_code, 200)

    def test_home(self):
        """Test the home view"""

        response = self.client.get(reverse("polls:home"))
        self.assertEqual(response.status_code, 200)

    def test_index(self):
        """Test the index view"""

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)

    def test_question(self):
        """Test the question view"""

        response = self.client.get(reverse("polls:question"))
        self.assertEqual(response.status_code, 200)

    def test_question_by_date(self):
        """Test the question view with a date"""

        # format yyyy-mm-dd
        response0 = self.client.get(reverse("polls:question", args=("2023-09-16",)))
        self.assertEqual(response0.status_code, 200)

        # format yyyy/mm/dd and check for context
        response1 = self.client.get(reverse("polls:question", args=("2023/09/16",)))
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(1, response1.context["questions"].count())
        self.assertIn("Question 1", response1.context["questions"][0].question_text)

        # empty queryset
        response2 = self.client.get(reverse("polls:question", args=("2024/09/16",)))
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(0, response2.context["questions"].count())

    def test_polls_detail(self):
        """Test the polls view"""

        response = self.client.get(reverse("polls:detail", args=(100,)))
        self.assertEqual(response.status_code, 200)

    def test_polls_results(self):
        """Test the polls view"""

        response = self.client.get(reverse("polls:results", args=(100,)))
        self.assertEqual(response.status_code, 200)

    def test_polls_vote(self):
        """Test the polls view"""

        response = self.client.get(reverse("polls:vote", args=(100,)))
        self.assertEqual(response.status_code, 200)

    def test_polls_vote_does_not_exist(self):
        """Test the polls view 404"""

        response = self.client.get(reverse("polls:vote", args=(200,)))
        self.assertEqual(response.status_code, 404)

    def test_polls_vote_with_valid_choice(self):
        """Test the polls view: vote with valid choice"""

        response = self.client.post(reverse("polls:vote", args=(100,)), {"choice": 200})
        self.assertEqual(response.status_code, 302)
        self.choice1.refresh_from_db()
        self.assertEqual(self.choice1.votes, 1)
        self.assertIn("voted_question_100", response.cookies)

    def test_polls_vote_with_invalid_choice(self):
        """Test the polls view: press vote without selecting a choice"""

        response = self.client.post(reverse("polls:vote", args=(100,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please select a choice.")

    def test_polls_view_cannot_vote_with_cookie_active(self):
        """Test the polls view: user cannot vote more than one. Cookie is set."""

        cookie_timestamp = (timezone.now() - timedelta(days=0)).strftime(
            "%a, %d-%b-%Y %H:%M:%S GMT"
        )
        response = self.client.get(
            reverse("polls:vote", args=(100,)),
            HTTP_COOKIE=f"voted_question_100={cookie_timestamp}",
        )  # valid cookie
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "You have already voted for this question. Please vote for another question.",
            response.context["error_message"],
        )

    def test_polls_vote_with_cookie_expired(self):
        """Test the polls view: user vote with a Cookie with more than 24 hrs."""

        cookie_timestamp = (timezone.now() - timedelta(days=2)).strftime(
            "%a, %d-%b-%Y %H:%M:%S GMT"
        )
        response = self.client.post(
            reverse("polls:vote", args=(100,)),
            {"choice": 201},
            HTTP_COOKIE=f"voted_question_100={cookie_timestamp}",
        )  # expired cookie
        self.assertEqual(response.status_code, 302)
        self.choice2.refresh_from_db()
        self.assertEqual(self.choice2.votes, 1)
