from json.decoder import JSONDecodeError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from question.models import Question, File, Submission, UserProfile, Course, Lesson, SubmissionFile, Bookmark
from question.forms import SubmissionFileForm, UploadFileForm, UploadForm, CreateCourseForm, CreateLessonForm
from django.forms.formsets import formset_factory
from django.forms.formsets import BaseFormSet
from django.urls import reverse
from django.contrib.auth.models import User
from django.core import serializers
from django.views import View
from django.db.utils import IntegrityError
import markdown as md
import json
import requests



# URL to submit questions
# API_URL = "http://192.168.56.103:8080/java/submit"
# API_URL = "http://192.168.0.17:8080/java/submit"
# API_URL = "http://localhost:8080/java/submit"
API_URL = "http://0.0.0.0:8080/java/submit"

# Homepage
class IndexView(View):

    def get(self, request):

        questions = Question.objects.all()

        # get most recently modified courses
        courses = Course.objects.order_by('created')[:5]

        context_dict = {
            'questions': questions,
            'courses': courses
        }

        lessons = []
        # bookmark_list = None

        if request.user.is_authenticated:
            # get user's submissions
            submissions = Submission.objects.filter(owner=request.user).order_by('-created')

            # list to store lessons (may include duplicates)
            dup_lessons = []

            for submission in submissions:
                dup_lessons.append(submission.question.lesson)

            # set to store lessons
            lesson_set = set()

            # list for unique lessons
            lessons = []

            # remove duplicated from list
            for l in dup_lessons:
                if l not in lesson_set:
                    lessons.append(l)
                    lesson_set.add(l)

            # get bookmarks
            bookmark_list = Bookmark.objects.filter(owner=request.user).order_by('-created')[:5]

            context_dict["bookmark_list"] = bookmark_list

        context_dict['lessons'] = lessons

        return render(request, 'question/index.html', context=context_dict)

# List of all courses
class CourseListView(View):

    def get(self, request):

        # list of courses
        courses = Course.objects.all()

        # form for new course
        form = CreateCourseForm()

        context_dict = {
            'courses': courses,
            'form': form,
        }

        return render(request, 'question/courses.html', context=context_dict)

    def post(self, request):

        form = CreateCourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.owner = request.user
            course.save()

            context_dict = {
                'course': course
            }

            return redirect(reverse('question:course',
                                    kwargs={'course_slug': course.slug}))

        else:
            return redirect(reverse('question:course_list'))


# def create_course(request):
#
#     if request.method == 'POST':
#
#         form = CreateCourseForm(request.POST)
#
#         if form.is_valid():
#             course = form.save(commit=False)
#             course.owner = request.user
#             course.save()
#
#         context_dict = {
#             'course': course
#         }
#
#         return redirect(reverse('question:lesson_list',
#                                 kwargs={'course_slug': course.slug}))
#
#     if request.method == 'GET':
#
#         form = CreateCourseForm()
#
#         context_dict = {
#             'form': form,
#         }
#
#         return render(request, 'question/createCourse.html', context=context_dict)

# Course (container for Lessons)
class CourseView(View):

    def get(self, request, course_slug):

        course_obj = Course.objects.get(slug=course_slug)
        lessons = Lesson.objects.filter(course=course_obj).order_by('position')

        form = CreateLessonForm()

        context_dict = {
            'lessons': lessons,
            'course': course_obj,
            'form': form,
        }

        return render(request, 'question/lessons.html', context=context_dict)

    def post(self, request, course_slug):

        course = Course.objects.get(slug=course_slug)

        form = CreateLessonForm(request.POST)

        if form.is_valid():

            # get other lessons in this course
            course_lessons = Lesson.objects.filter(course=course).order_by('position')

            # work out next position available
            if len(course_lessons) > 0:
                position = course_lessons[len(course_lessons) - 1].position + 1
            else:
                position = 1

            lesson = form.save(commit=False)
            lesson.owner = request.user
            lesson.course = course
            lesson.position = position

            # try to save, if unsuccessful reload page
            try:
                lesson.save()
            except IntegrityError:
                return redirect(reverse('question:course',
                                        kwargs={'course_slug': course.slug}))

        context_dict = {
            'course': course,
            'lesson': lesson
        }

        return redirect(reverse('question:lesson',
                                kwargs={'course_slug': course.slug,
                                        'lesson_slug': lesson.slug}))

    def delete(self, request, course_slug):

        # get course object from database
        course_obj = Course.objects.get(slug=course_slug)

        # delete course
        course_obj.delete()

        # get updated list of courses
        courses_updated = Course.objects.filter(owner=request.user)

        # convert to json
        courses_json = serializers.serialize('json', courses_updated)

        # return response
        return HttpResponse(courses_json, content_type='application/json')

# def create_lesson(request, course_slug):
#
#     course = Course.objects.get(slug=course_slug)
#
#     if request.method == 'POST':
#
#         form = CreateLessonForm(request.POST)
#
#         if form.is_valid():
#
#             # get other lessons in this course
#             course_lessons = Lesson.objects.filter(course=course).order_by('position')
#
#             # work out next position available
#             if len(course_lessons) > 0:
#                 position = course_lessons[len(course_lessons) - 1].position + 1
#             else:
#                 position = 1
#
#             lesson = form.save(commit=False)
#             lesson.owner = request.user
#             lesson.course = course
#             lesson.position = position
#             lesson.save()
#
#
#
#         context_dict = {
#             'course': course,
#             'lesson': lesson
#         }
#
#         return redirect(reverse('question:question_list',
#                                 kwargs={'course_slug': course.slug,
#                                         'lesson_slug': lesson.slug}))
#
#     if request.method == 'GET':
#
#         form = CreateLessonForm()
#
#         context_dict = {
#             'form': form,
#             'course': course
#         }
#
#         return render(request, 'question/createLesson.html', context_dict)

# Lesson (container for Questions)
class LessonView(View):

    def get(self, request, course_slug, lesson_slug):

        # get relevant objects from database
        course_obj = Course.objects.get(slug=course_slug)
        lesson_obj = Lesson.objects.get(slug=lesson_slug, course=course_obj)
        questions = Question.objects.filter(lesson=lesson_obj).order_by('position')

        context_dict = {
            'questions': questions,
            'lesson': lesson_obj,
            'course': course_obj,
        }

        return render(request, 'question/questions.html', context=context_dict)

    def delete(self, request, course_slug, lesson_slug):

        # get relevant objects from database
        course_obj = Course.objects.get(slug=course_slug)
        lesson_obj = Lesson.objects.get(slug=lesson_slug, course=course_obj)

        # get other lessons in this course
        course_lessons_qset = Lesson.objects.filter(course=course_obj).order_by('position')
        course_lessons = list(course_lessons_qset)
        index = course_lessons.index(lesson_obj)

        # for every question after current position,
        # set position to position on previous element
        sub_list = course_lessons[index:]

        for prev, curr in zip(reversed(sub_list[:-1]), reversed(sub_list)):
            curr.position = prev.position
            curr.save()

        lesson_obj.delete()

        # get updated list of lessons in this course
        course_lessons_updated = Lesson.objects.filter(course=course_obj).order_by('position')

        course_json = serializers.serialize('json', course_lessons_updated)

        return HttpResponse(course_json, content_type='application/json')

# Question
#
# Shows question descriptive information and initial source files/code
class QuestionView(View):

    def get(self, request, question_slug, lesson_slug, course_slug):

        # get model objects
        course_obj = Course.objects.get(slug=course_slug)
        lesson_obj = Lesson.objects.get(slug=lesson_slug, course=course_obj)
        question_obj = Question.objects.get(slug=question_slug, lesson=lesson_obj)
        files = File.objects.filter(question=question_obj)

        # check if bookmarked
        if request.user.is_authenticated:
            is_bookmarked = Bookmark.objects.filter(question=question_obj, owner=request.user)
        else:
            is_bookmarked = None

        # get questions in lesson
        lesson_questions_qset = Question.objects.filter(lesson=lesson_obj).order_by('position')
        lesson_questions = list(lesson_questions_qset)
        index = lesson_questions.index(question_obj)

        # get next question for 'next' button if there is one
        if index < (len(lesson_questions) - 1):
            next_question = lesson_questions[index + 1]
        else:
            next_question = None

        # set of forms for files
        SubmissionFileFormSet = formset_factory(SubmissionFileForm, formset=BaseFormSet, extra=0)

        formset_data = []

        for file in files:
            formset_data.append({
                'name': file.name,
                'contents': file.contents,
            })

        formset_context = SubmissionFileFormSet(initial=formset_data)

        # set solved to false by default
        has_solved = False

        # check if user has solved question already
        if request.user.is_authenticated:
            has_solved = Submission.objects.filter(question=question_obj,
                                                   owner=request.user).exists()

        # create context dict to pass to template
        context_dict = {
            'question': question_obj,
            'next_question': next_question,
            # actual forms
            # 'file_forms': file_forms
            'lesson': lesson_obj,
            'course': course_obj,
            'file_formset': formset_context,
            'is_bookmarked': is_bookmarked,
            'has_solved': has_solved,
        }

        # render question with default/original files
        return render(request, 'question/question.html', context=context_dict)

    # post an answer to question
    def post(self, request, course_slug, lesson_slug, question_slug):

        course = Course.objects.get(slug=course_slug)
        lesson = Lesson.objects.get(slug=lesson_slug, course=course)
        question_obj = Question.objects.get(slug=question_slug, lesson=lesson)

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

            if request.user.is_authenticated:
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

    # delete a question
    # returns an updated list of questions in the delete question's parent lesson
    def delete(self, request, question_slug, lesson_slug, course_slug):

        # get model objects
        course_obj = Course.objects.get(slug=course_slug)
        lesson_obj = Lesson.objects.get(slug=lesson_slug, course=course_obj)
        question_obj = Question.objects.get(slug=question_slug, lesson=lesson_obj)

        # get questions in lesson
        lesson_questions_qset = Question.objects.filter(lesson=lesson_obj).order_by('position')
        lesson_questions = list(lesson_questions_qset)
        index = lesson_questions.index(question_obj)

        # get other questions in this lesson
        lesson_questions_qset = Question.objects.filter(lesson=lesson_obj).order_by('position')
        lesson_questions = list(lesson_questions_qset)
        index = lesson_questions.index(question_obj)

        # for every question after current position,
        # set position to position on previous element
        sub_list = lesson_questions[index:]

        for prev, curr in zip(reversed(sub_list[:-1]), reversed(sub_list)):
            curr.position = prev.position
            curr.save()

        # delete question
        question_obj.delete()

        # get updated set of questions
        lesson_questions_updated = Question.objects.filter(lesson=lesson_obj).order_by('position')
        lesson_json = serializers.serialize('json', lesson_questions_updated)
        return HttpResponse(lesson_json, content_type="application/json")


# Helper function to handle API communication
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

# Editor page to allow new questions to be created and stored
class UploadView(View):

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.has_perm('question.can_create'), login_url="/"))
    def get(self, request, course_slug, lesson_slug):

        course = Course.objects.get(slug=course_slug)
        lesson = Lesson.objects.get(slug=lesson_slug, course=course)

        # if not owner, redirect to index
        if course.owner != request.user:
            return redirect("/")

        # set of forms for files
        UploadFileFormSet = formset_factory(UploadFileForm, formset=BaseFormSet, extra=0, can_delete=True)

        pre_load_questions = False

        if (pre_load_questions):
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
    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.has_perm('question.can_create'), login_url="/"))
    def post(self, request, course_slug, lesson_slug):

        course = Course.objects.get(slug=course_slug)
        lesson = Lesson.objects.get(slug=lesson_slug, course=course)

        # if not owner, redirect to index
        if course.owner != request.user:
            return redirect("/")

        owner = request.user

        # # Post request
        # if request.method == 'POST':

        # set of forms for files
        UploadFileFormSet = formset_factory(UploadFileForm, formset=BaseFormSet, extra=0, can_delete=True)

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

                # get other questions in this lesson
                lesson_questions = Question.objects.filter(lesson=lesson).order_by('position')

                # work out next position available
                if len(lesson_questions) > 0:
                    position = lesson_questions[len(lesson_questions) - 1].position + 1
                else:
                    position = 1

                question = Question.objects.get_or_create(name=cleaned_data['question_name'],
                                                          lesson=lesson,
                                                          owner=owner)

                # if question does not already exist
                if question[1]:
                    print("new question started")
                    question[0].position = position
                    question[0].testFile = cleaned_data['test_file']
                    question[0].description = cleaned_data['question_description']
                    question[0].save()

                    if formset.is_valid():
                        # loop from 2nd form (first is empty)
                        for f in formset[1:]:
                            cleaned_data = f.cleaned_data

                            if not cleaned_data['DELETE']:
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


# additional view function to check authors can solve uploaded questions
def ajax_solve(request, course_slug, lesson_slug):

    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug, course=course)

    # Post request
    if request.method == 'POST':
        # set of forms for files
        UploadFileFormSet = formset_factory(UploadFileForm, formset=BaseFormSet, extra=0, can_delete=True)

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


# Helper function to handle API communication
def send_to_API(formset, upload_form):
    # dict to send to API
    API_dict = {
        'files': []
    }

    if formset.is_valid():

        print("about to loop over deleted items")
        for obj in formset.deleted_forms:
            print(obj)
            # formset.remove(obj)

        # loop from 2nd form (first is empty)
        for f in formset[1:]:

            # if f not in formset.deleted_forms:
            cleaned_data = f.cleaned_data

            if not cleaned_data['DELETE']:
                API_dict['files'].append({
                    'name': cleaned_data['name'],
                    'content': cleaned_data['contents']
                })
            else:
                print("-- Deleted form: --")
                print(cleaned_data)


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


# function which takes request containing
# markdown text and returns it as html
def markdown_ajax(request):

    if request.method == 'POST':

        text = request.POST.get('description', None)

        # print(text)

        converted = md.markdown(text, extensions=['markdown.extensions.fenced_code'])

        # print(converted)

        return HttpResponse(converted)


# function to move question position within a course (via AJAX)
@transaction.atomic
def move_question_ajax(request, course_slug, lesson_slug, question_slug, direction):

    if(request.method == 'GET'):

        # get question and associated course & lesson
        course_obj = Course.objects.get(slug=course_slug)
        lesson_obj = Lesson.objects.get(slug=lesson_slug, course=course_obj)
        question_obj = Question.objects.get(slug=question_slug, lesson=lesson_obj)

        # get pos of this question
        this_pos = question_obj.position

        # get other questions in this lesson
        lesson_questions_qset = Question.objects.filter(lesson=lesson_obj).order_by('position')
        lesson_questions = list(lesson_questions_qset)
        index = lesson_questions.index(question_obj)

        # if moving selected question up
        if direction == 'up':
            print("up")
            # get question above this question and position
            prev_question_obj = lesson_questions[index - 1]
            prev_pos = prev_question_obj.position

            question_obj.position = prev_pos
            prev_question_obj.position = this_pos

            question_obj.save()
            prev_question_obj.save()

        # if moving selected question down
        elif direction == 'down':
            # get question below this question and position
            if index < len(lesson_questions) - 1:
                next_question_obj = lesson_questions[index + 1]
                next_pos = next_question_obj.position
            # if at end of list, set next question to first position
            else:
                next_question_obj = lesson_questions[0]
                next_pos = next_question_obj.position

            question_obj.position = next_pos
            next_question_obj.position = this_pos

            question_obj.save()
            next_question_obj.save()

        # get updated list of questions in this lesson
        lesson_questions_updated = Question.objects.filter(lesson=lesson_obj).order_by('position')

        lesson_json = serializers.serialize('json', lesson_questions_updated)

        return HttpResponse(lesson_json, content_type="application/json")


# function to move lesson position within a course (via AJAX)
def move_lesson_ajax(request, course_slug, lesson_slug, direction):

    if request.method == 'GET':

        # get lesson and associated course
        course_obj = Course.objects.get(slug=course_slug)
        lesson_obj = Lesson.objects.get(slug=lesson_slug, course=course_obj)

        # get pos of this question
        this_pos = lesson_obj.position

        # get other lessons in this course
        course_lessons_qset = Lesson.objects.filter(course=course_obj).order_by('position')
        course_lessons = list(course_lessons_qset)
        index = course_lessons.index(lesson_obj)

        # if moving selected lesson up
        if direction == 'up':

            # get lesson above this lesson and position
            prev_lesson_obj = course_lessons[index - 1]
            prev_pos = prev_lesson_obj.position

            lesson_obj.position = prev_pos
            prev_lesson_obj.position = this_pos

            lesson_obj.save()
            prev_lesson_obj.save()

        elif direction == 'down':

            # get lesson below this position and position
            if index < len(course_lessons) - 1:
                next_lesson_obj = course_lessons[index + 1]
                next_pos = next_lesson_obj.position
            # if at end of list, set next lesson to first position
            else:
                next_lesson_obj = course_lessons[0]
                next_pos = next_lesson_obj.position

            lesson_obj.position = next_pos
            next_lesson_obj.position = this_pos

            lesson_obj.save()
            next_lesson_obj.save()

        # get updated list of lessons in this course
        course_lessons_updated = Lesson.objects.filter(course=course_obj).order_by('position')

        course_json = serializers.serialize('json', course_lessons_updated)

        return HttpResponse(course_json, content_type='application/json')


# function to create a user profile
@login_required
def create_profile(request):
    user_profile = UserProfile.objects.get_or_create(user=request.user)
    user_profile[0].save()
    return redirect("/")


# User profile
class ProfileView(View):

    def get(self, request, username):

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect(reverse('index'))

        user_profile = UserProfile.objects.get_or_create(user=user)[0]

        user_courses = Course.objects.filter(owner=user)

        # get recent submissions
        submissions = Submission.objects.filter(owner=user).order_by('-created')[:5]
        recent_questions = []
        for submission in submissions:
            recent_questions.append(submission.question)

        # convert markdown to html
        # converted = md.markdown(user_profile.bio, extensions=['markdown.extensions.fenced_code'])

        context_dict = {
            'user_profile': user_profile,
            'selected_user': user,
            'user_courses': user_courses,
            'questions': recent_questions,
        }

        return render(request, 'question/profile.html', context_dict)


# function to update profile bio
@login_required
def update_profile(request):

    if request.method == 'POST':

        # get text
        text = request.POST.get('description', None)

        # update signed in user's profile
        profile = UserProfile.objects.get(user=request.user)
        profile.bio = text
        profile.save()

        # convert markdown to html
        converted = md.markdown(text, extensions=['markdown.extensions.fenced_code'])

        # return markdown converted to html
        return HttpResponse(converted)


# Bookmarks page
class BookmarksView(View):

    @method_decorator(login_required)
    def get(self, request):
        bookmark_list = Bookmark.objects.filter(owner=request.user)

        context_dict = {
            "bookmark_list": bookmark_list
        }

        return render(request, "question/bookmarks.html", context_dict)


# bookmark a question for current user (via AJAX)
@login_required
def bookmark_ajax(request, question_slug, lesson_slug, course_slug):

    # get question
    course_obj = Course.objects.get(slug=course_slug)
    lesson_obj = Lesson.objects.get(slug=lesson_slug, course=course_obj)
    question_obj = Question.objects.get(slug=question_slug, lesson=lesson_obj)

    # create bookmark
    if request.method == 'POST':

        # create bookmark
        bookmark = Bookmark.objects.get_or_create(question=question_obj, owner=request.user)
        bookmark[0].save()

        return HttpResponse("added")

    # delete bookmark
    if request.method == 'DELETE':

        # get and delete bookmark
        try:
            bookmark = Bookmark.objects.get(question=question_obj, owner=request.user)
            bookmark.delete()
        except Bookmark.DoesNotExist:
            bookmark = None

        return HttpResponse("deleted")
