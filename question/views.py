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

def question(request):

    # get question
    question_obj = Question.objects.get(name='arrayList')

    # testing
    question_dict = model_to_dict(question_obj)
    print(question_dict)

    # get files
    files = File.objects.filter(question=question_obj)

    file_forms = []

    for file in files:
        file_forms.append({'file': file, 'form': SubmissionFileForm(initial={'name': file.name, 'contents': file.contents})})
        # file_forms[file.name] = SubmissionFileForm(initial={'name': "test1", 'contents': "test2"})
        print('test', file.name, file.contents)

    form = SubmissionFileForm(initial={'name': "test1", 'contents': "test2"})

    # testing
    for file in files:
        file_dict = model_to_dict(file)
        print(file_dict)

    # create context dict to pass to template
    context_dict = {
        'question': question_obj,
        'files': files,
        # test only
        'form': form,
        # actual forms
        'file_forms': file_forms
    }

    return render(request, 'question/question.html', context=context_dict)
