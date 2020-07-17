from django.shortcuts import render
from django.http import HttpResponse
from question.models import Question, File, Submission
from question.forms import SubmissionFileForm
from django.forms.models import model_to_dict
from django.core import serializers
import json
import requests

# URL to submit questions
API_URL = "http://localhost:8080/java/submit"


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

    # get files
    files = File.objects.filter(question=question_obj)

    # Post request
    if(request.method == 'POST'):

        # Test form submission details
        # print(dict(request.POST.lists()))

        # list to store submitted forms
        form_submissions = [];

        # create submission object associated with post
        submission = Submission.objects.get_or_create(question=question_obj)
        submission[0].save()

        # list to store updated forms containing submitted files
        file_forms = []

        # dict to send to API
        API_dict = {
            'files': []
        }

        # build a form for each submitted file
        for i in range(files.count()):
            form_submissions.append(SubmissionFileForm(request.POST, prefix="file" + str(i)))

        # for each form, create a submission file and associate with current submission
        for i in range(files.count()):
            if form_submissions[i].is_valid():

                # create submission file
                submission_file = form_submissions[i].save(commit=False)

                # associate with current submission
                submission_file.submission = submission[0]

                # save
                submission_file.save()

                file_forms.append({'file': submission_file,
                                   'form': SubmissionFileForm(initial={'name': submission_file.name,
                                                                       'contents': submission_file.contents},
                                                              prefix="file" + str(i))})

                # add submitted files to submission dict
                API_dict['files'].append({
                    'name': submission_file.name,
                    'content': submission_file.contents
                })

                API_dict['files'].append({
                    'name': "Tests.java",
                    'content': question_obj.testFile
                })

        # print("To send to API: " + json.dumps(API_dict))

        results = requests.post(url=API_URL, json=API_dict)

        print(results.content)

        # create context dict to pass to template
        context_dict = {
            'question': question_obj,
            # actual forms
            'file_forms': file_forms
        }

        # render page showing submitted files
        return render(request, 'question/question.html', context=context_dict)

    # Get request
    if (request.method == 'GET'):

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

        # render question with default/original files
        return render(request, 'question/question.html', context=context_dict)


