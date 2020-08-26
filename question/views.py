from json.decoder import JSONDecodeError

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.http import HttpResponse
from question.models import Question, File, Submission, UserProfile, Course, Lesson, SubmissionFile
from question.forms import SubmissionFileForm, UploadFileForm, UploadForm, UserForm, UserProfileForm, CreateCourseForm, \
    CreateLessonForm
from django.forms.models import model_to_dict
import json
import requests
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet
from django.urls import reverse
from django.contrib.auth.models import User


# URL to submit questions
# API_URL = "http://192.168.56.103:8080/java/submit"
API_URL = "http://192.168.0.17:8080/java/submit"
# API_URL = "http://localhost:8080/java/submit"


def index(request):

    questions = Question.objects.all()

    # get most recently modified courses
    courses = Course.objects.order_by('created')[:5]

    context_dict = {
        'questions': questions,
        'courses': courses
    }

    lessons = []

    if request.user.is_authenticated:
        # get user's submissions
        submissions = Submission.objects.filter(owner=request.user)

        for submission in submissions:
            lessons.append(submission.question.lesson)

    context_dict['lessons'] = lessons


    return render(request, 'question/index.html', context=context_dict)


def course_list(request):

    courses = Course.objects.all()

    context_dict = {
        'courses': courses
    }

    return render(request, 'question/courses.html', context=context_dict)


def create_course(request):

    if request.method == 'POST':

        form = CreateCourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()

        context_dict = {
            'course': course
        }

        return redirect(reverse('question:lesson_list',
                                kwargs={'course_slug': course.slug}))

    if request.method == 'GET':

        form = CreateCourseForm()

        context_dict = {
            'form': form,
        }

        return render(request, 'question/createCourse.html', context=context_dict)


def lesson_list(request, course_slug):

    course = Course.objects.get(slug=course_slug)
    lessons = Lesson.objects.filter(course=course)

    context_dict = {
        'lessons': lessons,
        'course': course,
    }

    return render(request, 'question/lessons.html', context=context_dict)


def create_lesson(request, course_slug):

    course = Course.objects.get(slug=course_slug)

    if request.method == 'POST':

        form = CreateLessonForm(request.POST)

        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.owner = request.user
            lesson.course = course
            lesson.save()



        context_dict = {
            'course': course,
            'lesson': lesson
        }

        return redirect(reverse('question:question_list',
                                kwargs={'course_slug': course.slug,
                                        'lesson_slug': lesson.slug}))

    if request.method == 'GET':

        form = CreateLessonForm()

        context_dict = {
            'form': form,
            'course': course
        }

        return render(request, 'question/createLesson.html', context_dict)


def question_list(request, course_slug, lesson_slug):
    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug, course=course)
    questions = Question.objects.filter(lesson=lesson)

    context_dict = {
        'questions': questions,
        'lesson': lesson,
        'course': course,
    }

    return render(request, 'question/questions.html', context=context_dict)


def question(request, question_slug, lesson_slug, course_slug):

    # get model objects
    course_obj = Course.objects.get(slug=course_slug)
    lesson_obj = Lesson.objects.get(slug=lesson_slug, course=course_obj)
    question_obj = Question.objects.get(slug=question_slug, lesson=lesson_obj)
    files = File.objects.filter(question=question_obj)

    # set of forms for files
    SubmissionFileFormSet = formset_factory(SubmissionFileForm, formset=BaseFormSet, extra=0)

    # Get request
    if request.method == 'GET':

        formset_data = []

        for file in files:
            formset_data.append({
                'name': file.name,
                'contents': file.contents,
            })

        formset_context = SubmissionFileFormSet(initial=formset_data)

        # create context dict to pass to template
        context_dict = {
            'question': question_obj,
            # actual forms
            # 'file_forms': file_forms
            'file_formset': formset_context
        }

        # render question with default/original files
        return render(request, 'question/question.html', context=context_dict)


def question_ajax(request, course_slug, lesson_slug, question_slug):

    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug, course=course)
    question_obj = Question.objects.get(slug=question_slug, lesson=lesson)

    # Post request
    if request.method == 'POST':
        # set of forms for files
        SubmissionFileFormSet = formset_factory(SubmissionFileForm, formset=BaseFormSet, extra=0)

        # get posted formset
        formset = SubmissionFileFormSet(request.POST)

        API_dict = {
            'files': []
        }

        # file data for send back to client for page refresh
        formset_data = []

        if formset.is_valid():

            for f in formset:

                cleaned_data = f.cleaned_data

                API_dict['files'].append({
                    'name': cleaned_data['name'],
                    'content': cleaned_data['contents']
                })

                formset_data.append({
                    'name': cleaned_data['name'],
                    'contents': cleaned_data['contents']
                })

            # add test file to API submission
            API_dict['files'].append({
                'name': 'Tests.java',
                'content': question_obj.testFile
            })
        else:
            print(formset.errors)

        # make API request, returns object to be returned to client
        json_return_object = submit_to_API(API_dict)

        # if all tests pass, create submission to store
        if json_return_object['summaryCode'] == 0:

            # remove any existing submissions
            existing_submissions = Submission.objects.filter(owner=request.user,
                                                             question=question_obj)

            # remove any files associated with existing submissions
            for sub in existing_submissions:
                existing_submission_files = SubmissionFile.objects.filter(submission=sub)
                existing_submission_files.delete()

            # remove submissions
            existing_submissions.delete()

            # create submission associated with question
            submission = Submission.objects.create(question=question_obj,
                                                   owner=request.user)
            submission.save()

            # create files and associate with submission
            for file in API_dict['files']:

                print(file)

                submissionFile = SubmissionFile.objects.create(submission=submission,
                                                               name=file['name'],
                                                               contents=file['content'])
                submissionFile.save()

        # return results
        return HttpResponse(json.dumps(json_return_object))


# Helper method to handle API communication
def submit_to_API(API_dict):

            # testing
            # print("API_dict:\n" + json.dumps(API_dict))

            # make request
            results = requests.post(url=API_URL, json=API_dict)

            # print("Actual request response:\n" + str(results.content))

            decodedResults = results.content.decode('utf-8')

            # get results
            json_results = json.loads(decodedResults)

            # print("Decoded:\n" + str(json_results))

            # code to summarize test results status
            #   0 - all tests passed
            #   1 - all tests failed
            #   2 - mixture of tests failed/passed
            #   3 - no tests present
            summary_code = 3

            # separate output and error and decode inner JSON string
            try:
                output = json.loads(json_results['output'])

                if output['numTests'] == 0:
                    summary_code = 3
                elif output['numFailed'] == 0:
                    summary_code = 0
                elif output['numFailed'] == output['numTests']:
                    summary_code = 1
                else:
                    summary_code = 2

            except JSONDecodeError:
                output = json_results['output']

            # print("Output:\n" + str(output))

            errors = json_results["errors"]
            # print("Output:\n" + str(errors))

            # reconstruct object for return
            json_return_object = {
                'output': output,
                'errors': errors,
                'summaryCode': summary_code,
            }

            print("Json return object:\n" + str(json_return_object))

            return json_return_object


@login_required
@user_passes_test(lambda u: u.has_perm('question.can_create'), login_url="/")
def upload(request, course_slug, lesson_slug):

    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug, course=course)

    # set of forms for files
    UploadFileFormSet = formset_factory(UploadFileForm, formset=BaseFormSet, extra=0)

    pre_load_questions = True



    if(pre_load_questions):

        pre_load_course = Course.objects.get(name="Java Basics")
        pre_load_lesson = Lesson.objects.get(name="Methods", course=pre_load_course)

        # get question
        question_obj = Question.objects.get(slug="calculator",
                                            lesson=pre_load_lesson)

        # get files
        files = File.objects.filter(question=question_obj)

    # Get request
    if request.method == 'GET':

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
            'course': course,
            'lesson': lesson,
        }

        return render(request, 'question/upload.html', context_dict)


# Method to handle AJAX request to create new question
#
# Summary codes (json_return_object['summaryCode']):
#
#        0 - all tests passed
#        1 - all tests failed
#        2 - mixture of tests failed/passed
#        3 - no tests present
#        4 - question name already taken
#
@login_required
@user_passes_test(lambda u: u.has_perm('question.can_create'), login_url="/")
def ajax_upload(request, course_slug, lesson_slug):

    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug, course=course)

    owner = request.user

    # Post request
    if request.method == 'POST':

        # set of forms for files
        UploadFileFormSet = formset_factory(UploadFileForm, formset=BaseFormSet, extra=0)

        # testing
        decoded = request.body.decode('utf-8')
        print(decoded)

        formset = UploadFileFormSet(request.POST)
        upload_form = UploadForm(request.POST)

        # make API request, returns object to be returned to client
        json_return_object = send_to_API(formset, upload_form)

        # boolean to track whether a new question has been created
        json_return_object['uploaded'] = False

        if upload_form.is_valid():
            # get form data
            cleaned_data = upload_form.cleaned_data
            # if valid for saving (all tests failing)
            if json_return_object['summaryCode'] == 1:
                print("Upload form name:" + str(cleaned_data['question_name']))
                question = Question.objects.get_or_create(name=cleaned_data['question_name'],
                                                          lesson=lesson,
                                                          owner=owner)


                # if question does not already exist
                if question[1]:
                    print("new question started")

                    question[0].testFile = cleaned_data['test_file']
                    question[0].description = cleaned_data['question_description']
                    question[0].save()

                    if formset.is_valid():
                        # loop from 2nd form (first is empty)
                        for f in formset[1:]:
                            cleaned_data = f.cleaned_data
                            file = File.objects.create(name=cleaned_data['name'],
                                                       contents=cleaned_data['contents'],
                                                       question=question[0])
                            file.save()

                            json_return_object['uploaded'] = True
                else:
                    json_return_object['summaryCode'] = 4

        print("just before responding: \n" + str(json_return_object))

        # resturn results as json
        return HttpResponse(json.dumps(json_return_object))


def ajax_solve(request, course_slug, lesson_slug):

    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug, course=course)

    # Post request
    if request.method == 'POST':
        # set of forms for files
        UploadFileFormSet = formset_factory(UploadFileForm, formset=BaseFormSet, extra=0)

        # testing
        decoded = request.body.decode('utf-8')
        print(decoded)
        

        formset = UploadFileFormSet(request.POST)
        upload_form = UploadForm(request.POST)

        # make API request, returns object to be returned to client
        json_return_object = send_to_API(formset, upload_form)

        if upload_form.is_valid():
            # get form data
            cleaned_data = upload_form.cleaned_data
            # if valid for saving (all tests failing)
            if json_return_object['summaryCode'] == 0:

                # get question and set solved
                question = Question.objects.get_or_create(name=cleaned_data['question_name'],
                                                          lesson=lesson)
                question[0].solved = True
                question[0].save()

        return HttpResponse(json.dumps(json_return_object))


# Helper method to handle API communication
def send_to_API(formset, upload_form):
    # dict to send to API
    API_dict = {
        'files': []
    }

    if formset.is_valid():

        # loop from 2nd form (first is empty)
        for f in formset[1:]:
            cleaned_data = f.cleaned_data

            API_dict['files'].append({
                'name': cleaned_data['name'],
                'content': cleaned_data['contents']
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

            print("Actual request response:\n" + str(results.content))

            decodedResults = results.content.decode('utf-8')

            # get results
            json_results = json.loads(decodedResults)

            print("Decoded:\n" + str(json_results))

            # code to summarize test results status
            #   0 - all tests passed
            #   1 - all tests failed
            #   2 - mixture of tests failed/passed
            #   3 - no tests present
            summary_code = 3

            # separate output and error and decode inner JSON string
            try:
                output = json.loads(json_results['output'])

                if output['numTests'] == 0:
                    summary_code = 3
                elif output['numFailed'] == 0:
                    summary_code = 0
                elif output['numFailed'] == output['numTests']:
                    summary_code = 1
                else:
                    summary_code = 2

            except JSONDecodeError:
                output = json_results['output']

            print("Output:\n" + str(output))

            errors = json_results["errors"]
            print("Output:\n" + str(errors))

            # reconstruct object for return
            json_return_object = {
                'output': output,
                'errors': errors,
                'summaryCode': summary_code,
            }

            print("Json return object:\n" + str(json_return_object))

            return json_return_object

        else:
            print(upload_form.errors)
            return None

        # make request
        # results = requests.post(url=API_URL, json=API_dict)
    else:
        print(formset.errors)
        return None


@login_required
def create_profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)
    user_profile[0].save()
    return redirect(index)


def view_profile(request, username):

    if request.method == 'GET':
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect(reverse('index'))

        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        user_courses = Course.objects.filter(owner=request.user)

        context_dict = {
            'user_profile': user_profile,
            'selected_user': user,
            'user_courses': user_courses,
        }

        return render(request, 'question/profile.html', context_dict)
