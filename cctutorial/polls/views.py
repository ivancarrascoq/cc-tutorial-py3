import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from polls.models import Choice, Question


def index(request):
    latest_question_list = Question.objects.only('question_text').order_by('-pub_date')[:5]
    output = ', '.join([p.question_text for p in latest_question_list])
    return HttpResponse(output)


def most_popular_choice(request):
    """
    After you have created a series of questions and choices,
    return the choice with the most votes of all choices. If there
    are multiples with the same number of votes, return al. For
    the choice, display the choice_text, number of votes and
    related Question id in the response below.
    """
    return HttpResponse("")


def choices(request, pk=14):
    """
    If a primary key is passed in, return only that choice object.
    If no primary key is passed in, return all choices ordered by highest number of votes first.

    Show the related question in both instances
    """
    if pk:
        choice = Choice.objects.get(pk=pk)
        rendered = render_to_string('choices.html', {'choice': choice})
        return HttpResponse(rendered)
    else:
        choices = Choice.objects.all().order_by('pk')
        questions = []
        for choice in choices:
            question = Question.objects.get(pk=choice.question_id)
            questions.append(question)

        rendered = render_to_string('choices.html', {'choices': choices, 'questions': questions})
        return HttpResponse(rendered)


def question(request, pub_date=datetime.date.today()):
    """
    If a primary key is passed in, return only that choice object.
    If no primary key is passed in, return all choices ordered by highest number of votes first.

    Show the related question in both instances
    """

    questions = Question.objects.filter(pub_date=pub_date)

    rendered = render_to_string('questions.html', {'questions': questions})
    return HttpResponse(rendered)
