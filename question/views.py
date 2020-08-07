from django.shortcuts import render
from django.http import HttpResponse
from question.models import Question, File, Submission
from question.forms import SubmissionFileForm, UploadFileForm, UploadForm
from django.forms.models import model_to_dict
from django.core import serializers
import json
import requests
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet

# URL to submit questions
API_URL = "http://localhost:8080/java/submit"


def index(request):

    questions = Question.objects.all()


    context_dict = {
        'questions': questions
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

                # add the test file
                API_dict['files'].append({
                    'name': "Tests.java",
                    'content': question_obj.testFile
                })

        # print("To send to API: " + json.dumps(API_dict))

        # make request
        results = requests.post(url=API_URL, json=API_dict)

        print(results.content)

        # get results
        json_results = json.loads(results.content)

        print(json_results)

        # deserialize sub-object
        try:
            json_output = json.loads(json_results['output'])
        except ValueError:
            json_output = json_results['output']

        json_errors = json_results['errors']

        # create context dict to pass to template
        context_dict = {
            # question
            'question': question_obj,

            # actual forms
            'file_forms': file_forms,

            # json results
            'output': json_output,

            # json errors
            'errors': json_errors
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


def upload(request):

    # set of forms for files
    UploadFileFormSet = formset_factory(UploadFileForm, formset=BaseFormSet, extra=0)

    pre_load_questions = True

    if(pre_load_questions):

        # get question
        question_obj = Question.objects.get(slug="calculator")

        # get files
        files = File.objects.filter(question=question_obj)

    if request.method == 'POST':

        #testing
        decoded = request.body.decode('utf-8')
        print(decoded)

        formset = UploadFileFormSet(request.POST)
        upload_form = UploadForm(request.POST)

        # print("Upload form:" + str(upload_form))

        # dict to send to API
        API_dict = {
            'files': []
        }

        # data for context dict

        # populate formset with first empty/hidden entry
        formset_data = [{
                'name': "File",
                'contents': "<write file contents here>",
            },
        ]
        form_data = None

        if formset.is_valid():

            # loop from 2nd form (first is empty)
            for f in formset[1:]:

                cleaned_data = f.cleaned_data

                API_dict['files'].append({
                    'name': cleaned_data['name'],
                    'content': cleaned_data['contents']
                })

                formset_data.append({
                    'name': cleaned_data['name'],
                    'contents': cleaned_data['contents']
                })



            if upload_form.is_valid():

                # get form data
                cleaned_data = upload_form.cleaned_data

                print("Cleaned:\n" + str(cleaned_data))

                # add test to dictionary
                API_dict['files'].append({
                    'name': "Tests.java",
                    'content': cleaned_data['test_file'],
                })

                # testing
                print("API_dict:\n" + json.dumps(API_dict))

                # make request
                results = requests.post(url=API_URL, json=API_dict)

                # get results
                json_results = json.loads(results.content)

                print("Results from compiler:\n" + str(json_results))

                form_data = {
                    'question_name': cleaned_data['question_name'],
                    'question_description': cleaned_data['question_description'],
                    'test_file': cleaned_data['test_file'],
                }

            else:
                print(upload_form.errors)



            # make request
            # results = requests.post(url=API_URL, json=API_dict)
        else:
            print(formset.errors)



        # upload_form = UploadForm(request.POST)

        # populate context dict forms with uploaded data
        formset_context = UploadFileFormSet(initial=formset_data)
        form_context = UploadForm(initial=form_data)
        context_dict = {
            'upload_form': form_context,
            'upload_file_formset': formset_context,
        }

        return render(request, 'question/upload.html', context_dict)

    # Get request
    if (request.method == 'GET'):

        if pre_load_questions:

            formset_data = [{
                'name': "File",
                'contents': "<write file contents here>",
            },
            ]

            for file in files:
                formset_data.append({
                    'name': file.name,
                    'contents': file.contents
                })

            form_data = {
                'question_name': question_obj.name,
                'question_description': question_obj.description,
                'test_file': question_obj.testFile
            }

            formset_context = UploadFileFormSet(initial=formset_data)

            # form for rest of question data
            form_context = UploadForm(initial=form_data)
        else:

            formset_context = UploadFileFormSet(initial=[
                {
                    'name': "File",
                    'contents': "<write file contents here>",
                },
                {
                'name': "FileName.java",
                 'contents': "<write file contents here>",
                 },
            ])

            # form for rest of question data
            form_context = UploadForm(initial={
                'question_name': "{Question-name}",
                'question_description': "{Text-describing question}",
                'test_file': 'import static org.junit.Assert.*;\n' +
                             'import org.junit.Test;\n\n' +
                             'public class Tests{\n\n}'
            })

        context_dict = {
            'upload_form': form_context,
            'upload_file_formset': formset_context,
        }

        return render(request, 'question/upload.html', context_dict)


def ajax_test(request):

    # set of forms for files
    UploadFileFormSet = formset_factory(UploadFileForm, formset=BaseFormSet, extra=0)

    # Get request
    if (request.method == 'GET'):
        print("Get request received.")

        return HttpResponse("http response from GET call")

    # Post request
    if (request.method == 'POST'):

        # testing
        decoded = request.body.decode('utf-8')
        print(decoded)

        formset = UploadFileFormSet(request.POST)
        upload_form = UploadForm(request.POST)

        # print("Upload form:" + str(upload_form))

        # dict to send to API
        API_dict = {
            'files': []
        }

        # data for context dict

        # populate formset with first empty/hidden entry
        formset_data = [{
            'name': "File",
            'contents': "<write file contents here>",
        },
        ]
        form_data = None

        if formset.is_valid():

            # loop from 2nd form (first is empty)
            for f in formset[1:]:
                cleaned_data = f.cleaned_data

                API_dict['files'].append({
                    'name': cleaned_data['name'],
                    'content': cleaned_data['contents']
                })

                formset_data.append({
                    'name': cleaned_data['name'],
                    'contents': cleaned_data['contents']
                })

            if upload_form.is_valid():

                # get form data
                cleaned_data = upload_form.cleaned_data

                print("Cleaned:\n" + str(cleaned_data))

                # add test to dictionary
                API_dict['files'].append({
                    'name': "Tests.java",
                    'content': cleaned_data['test_file'],
                })

                # testing
                print("API_dict:\n" + json.dumps(API_dict))

                # make request
                results = requests.post(url=API_URL, json=API_dict)

                # get results
                json_results = json.loads(results.content)

                print("Results from compiler:\n" + str(json_results))

                form_data = {
                    'question_name': cleaned_data['question_name'],
                    'question_description': cleaned_data['question_description'],
                    'test_file': cleaned_data['test_file'],
                }

            else:
                print(upload_form.errors)

            # make request
            # results = requests.post(url=API_URL, json=API_dict)
        else:
            print(formset.errors)

        # upload_form = UploadForm(request.POST)

        # populate context dict forms with uploaded data
        formset_context = UploadFileFormSet(initial=formset_data)
        form_context = UploadForm(initial=form_data)
        context_dict = {
            'upload_form': form_context,
            'upload_file_formset': formset_context,
        }

        return HttpResponse("http response from POST call")
