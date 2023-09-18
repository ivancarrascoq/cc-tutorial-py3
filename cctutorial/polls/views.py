from datetime import datetime, timedelta
from collections import defaultdict
from .models import Choice, Question
from django.db.models import F, Max

# from django.db.models.functions import Coalesce
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages


def home(request):
    return render(request, "home.html")  # add reverse() URL for home


# polls
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    response = HttpResponse()
    response.delete_cookie("voted_date")
    return render(request, "polls/index.html", context)


def most_popular_choice(request):
    """
    After you have created a series of questions and choices,
    return the choice with the most votes of all choices. If there
    are multiples with the same number of votes, return al. For
    the choice, display the choice_text, number of votes and
    related Question id in the response below.
    """
    # max_votes = Choice.objects.aggregate(max_votes=Coalesce(Max('votes'), 0))['max_votes']
    max_votes = Choice.objects.aggregate(max_votes=Max("votes"))["max_votes"]
    popular_choices = Choice.objects.filter(votes=max_votes).values(
        "choice_text", "votes", "question"
    )
    # add exception and when no value is found
    context = {"popular_choices": popular_choices}
    return render(request, "polls/popular.html", context)


def choices(request, pk=None):
    """
    If a primary key is passed in, return only that choice object.
    If no primary key is passed in, return all choices ordered by the highest number of votes first.

    Show the related question in both instances.
    """
    if pk:
        try:
            selected_choice = Choice.objects.get(pk=int(pk))
            # selected_choice = get_object_or_404(Choice, pk=int(pk))
            related_question = selected_choice.question
            related_choices = Choice.objects.filter(question=related_question).order_by("-votes")
            context = {"choices": related_choices, "question": related_question}
            return render(request, "polls/choices.html", context)
        except Choice.DoesNotExist:
            messages.add_message(request, messages.ERROR, "Choice does not exist.")
            return render(
                request,
                "polls/choices.html",
                status=404)

    else:
        all_choices = (
            Choice.objects.all()
            .values("choice_text", "votes", question_text=F("question__question_text"))
            .order_by("-votes")
        )
        questions = defaultdict(list)
        for i in all_choices:
            question_t = i["question_text"]
            choices_t = {"choice_text": i["choice_text"], "votes": i["votes"]}
            questions[question_t].append(choices_t)
        context = {"questions": dict(questions)}
        return render(request, "polls/choices.html", context)


def question(request, pub_date=None):
    """
    If a primary key is passed in, return only that choice object.
    If no primary key is passed in, return all choices ordered by highest number of votes first.

    Show the related question in both instances
    """

    if pub_date:
        pub_date = pub_date.replace("/", "-")
        year, month, day = map(int, pub_date.split("-"))
        pub_date_converted = timezone.datetime(year, month, day)
        questions = Question.objects.filter(pub_date__date=pub_date_converted)
    else:
        pub_date = timezone.now().date()
        questions = Question.objects.filter(pub_date__date=pub_date)
    context = {"questions": questions}
    return render(request, "polls/questions.html", context)


# tutorial
def detail(request, question_id):
    """
    Not used. This is from the tutorial.
    """
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    """
    Not used. This is from the tutorial.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question_pk = get_object_or_404(Question, pk=question_id)
    cookie_name = f"voted_question_{question_id}"
    cookie = request.COOKIES.get(cookie_name, False)
    try:
        selected_choice = question_pk.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        if _validate_cookie_for_voting(cookie):
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question_pk,
                    "error_message": "Please select a choice.",
                },
            )
        return render(
            request,
            "polls/detail.html",
            {
                "question": question_pk,
                "error_message": "You have already voted for this question. Please vote for another question.",
            },
        )
    else:  # POST request
        if _validate_cookie_for_voting(cookie):
            selected_choice.votes += 1
            selected_choice.save()
            response = HttpResponseRedirect(
                reverse("polls:results", args=(question_id,))
            )
            response.set_cookie(
                cookie_name, timezone.now().strftime("%a, %d-%b-%Y %H:%M:%S GMT")
            )
            return response
        return render(
            request,
            "polls/detail.html",
            {
                "question": question_pk,
                "error_message": "You have already voted for this question. Please vote for another question.",
            },
        )


def _validate_cookie_for_voting(cookie: str):
    """
    return True if cookie expired, more than 24 hours, the user can vote
    return False if cookie is valid, less than 24 hours, the user can't vote
    """
    try:
        cookie_datetime = datetime.strptime(cookie, '%a, %d-%b-%Y %H:%M:%S GMT')  # change to timezone
        cookie_datetime = timezone.make_aware(cookie_datetime, timezone.utc)
        time_difference = timezone.now() - cookie_datetime
        one_day = timedelta(days=1)
        if time_difference > one_day:
            return True
        return False
    except (ValueError, TypeError):
        return True
