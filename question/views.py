from django.shortcuts import render
from django.http import HttpResponse
from question.models import Question, File
from question.forms import SubmissionFileForm
from django.forms.models import model_to_dict
from django.core import serializers


def index(request):

    context_dict = {
    }

    return render(request, 'question/index.html', context=context_dict)


# def question_list(request):
#
#     questions = Question.objects.all()
#
#     context_dict = {
#         'questions': []
#     }
#
#     for question in questions:
#         context_dict['questions'].append(question)
#
#     return render(request, 'question/index.html', context=context_dict)

def question(request, question_slug):

    # get question
    question_obj = Question.objects.get(slug=question_slug)

    if(request.method == 'POST'):
        print(dict(request.POST.lists()))



    # # testing
    # question_dict = model_to_dict(question_obj)
    # print(question_dict)

    # get files
    files = File.objects.filter(question=question_obj)

    file_forms = []

    # loop through files, enumerate to give index to use for prefix
    for counter, file in enumerate(files):
        #  store each file, along with a form, pre-populated with that file's name and contents
        # set prefix to differentiate forms on frontend
        file_forms.append({'file': file, 'form': SubmissionFileForm(initial={'name': file.name, 'contents': file.contents}, prefix="file" + str(counter))})
        # print('test', file.name, file.contents)

    # testing
    for file in files:
        file_dict = model_to_dict(file)
        # print(file_dict)

    # create context dict to pass to template
    context_dict = {
        'question': question_obj,
        # actual forms
        'file_forms': file_forms
    }

    return render(request, 'question/question.html', context=context_dict)
