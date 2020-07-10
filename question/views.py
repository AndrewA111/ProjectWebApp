from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context_dict = {'boldmessage': 'Test message'}
    return render(request, 'question/question.html', context=context_dict)