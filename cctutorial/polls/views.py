import datetime
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from .models import Choice, Question
from django.db.models import F, Max

# from django.db.models.functions import Coalesce
from collections import defaultdict


def home(request):
    return render(request, "home.html")  # add reverse() URL for home


def index(request):
    latest_question_list = Question.objects.all().order_by("-pub_date")[:5]
    rendered = render_to_string("index.html", {"latest": latest_question_list})
    return HttpResponse(rendered)


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
    rendered = render_to_string("popular.html", context)
    return HttpResponse(rendered)
    # return JsonResponse(list(popular_choices), safe=False, status=200)


# def choices(request, pk=None):
#     """
#     If a primary key is passed in, return only that choice object.
#     If no primary key is passed in, return all choices ordered by highest number of votes first.

#     Show the related question in both instances
#     """
#     # Show a short messages if either choices or questions are not available in the polls/choices view.

#     if pk:
#         choice = Choice.objects.filter(pk=pk).values('choice_text', 'votes', question_text= F('question__question_text'))
#         if choice.exists():
#             return JsonResponse(list(choice), status=200, safe=False)
#         else:
#             return JsonResponse({'error': 'Choice not found'}, status=404)
#     else:
#         choices = Choice.objects.all().values('choice_text', 'votes', question_text= F('question__question_text')).order_by('-votes')
#         return JsonResponse(list(choices), safe=False, status=200)


def choices(request, pk=None):
    """
    If a primary key is passed in, return only that choice object.
    If no primary key is passed in, return all choices ordered by the highest number of votes first.

    Show the related question in both instances.
    """
    if pk:
        selected_choice = Choice.objects.filter(pk=pk)
        if selected_choice.exists() and selected_choice[0].question:
            related_question = selected_choice[0].question
            related_choices = Choice.objects.filter(question=related_question).order_by(
                "-votes"
            )
            context = {"choices": related_choices, "question": related_question}
            return render(request, "choices.html", context)
        else:
            return HttpResponse("Choice not found", status=404)
    else:
        all_choices = (
            Choice.objects.all()
            .values("choice_text", "votes", question_text=F("question__question_text"))
            .order_by("-votes")
        )

        questions = defaultdict(list)
        for i in all_choices:
            question = i["question_text"]
            choices = {"choice_text": i["choice_text"], "votes": i["votes"]}
            questions[question].append(choices)
        context = {"questions": dict(questions)}
        return render(request, "choices.html", context)


def question(request, pub_date=str(timezone.now().date())):
    """
    If a primary key is passed in, return only that choice object.
    If no primary key is passed in, return all choices ordered by highest number of votes first.

    Show the related question in both instances
    """
    pub_date = pub_date.replace("/", "-")
    year, month, day = map(int, pub_date.split("-"))
    pub_date_converted = datetime.date(year, month, day)

    questions = Question.objects.filter(pub_date__date=pub_date_converted)
    rendered = render_to_string("questions.html", {"questions": questions})
    return HttpResponse(rendered)
