import os

from django.contrib.auth import get_user_model

import project_web_app.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_web_app.settings')

import django
django.setup()

import pprint
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from question.models import File, Question, Course, Lesson
from django.db import models



def populate():

    # Permissions

    # Group
    content_type = ContentType.objects.get(app_label="question", model="question")
    permission = Permission.objects.create(codename='can_create',
                                           name="Can create content",
                                           content_type=content_type)

    create_group = Group.objects.create(name="creator_group")
    create_group.permissions.add(permission)

    # Admin
    admin = User.objects.create_user('admin', 'noreply@apple.com', 'HelloWorld123')
    admin.is_staff = True
    admin.is_admin = True
    admin.is_superuser = True
    admin.save()

    student_user = User.objects.create_user(username='andrew', email="a@a.com", password="HelloWorld123")

    tutor_user = User.objects.create_user(username='Tutor123', email="j@a.com", password="SurveyPass123")
    tutor_user.groups.add(create_group)

    root = project_web_app.settings.BASE_DIR
    courses = os.path.join(root, 'questionFiles')

    # iterate through courses, lessons and questions
    for course in getFolderNames(courses):

        # create course
        course_obj = add_course(course, tutor_user)

        # get lessons in course
        lessons = os.path.join(courses, course)

        for lesson in getFolderNames(lessons):

            # create lesson
            lesson_obj = add_lesson(lesson, tutor_user, course_obj)

            # get questions
            questions = os.path.join(lessons, lesson)

            for questionDir in getFolderNames(questions):

                # get question dir path
                questionPath = os.path.join(questions, questionDir)

                # read relevant files from dir
                questionDetails = readQuestionFiles(questionPath)

                # pretty print data for debugging
                # pprint.pprint(questionDetails)

                # get description
                description = readFile("description.txt", questionPath)

                # make question
                question = add_question(questionDir, tutor_user, lesson_obj, questionDetails['testFile']['contents'], description)

                # loop through files and create file objects
                for file in questionDetails['questionFiles']:
                    add_file(question, file['name'], file['contents'])


def add_course(name, owner):
    c, created = Course.objects.get_or_create(name=name,
                                              owner=owner)
    c.save()
    return c


def add_lesson(name, owner, course):

    # get other lessons in this course
    course_lessons = Lesson.objects.filter(course=course).order_by('position')

    # work out next position available
    if len(course_lessons) > 0:
        position = course_lessons[len(course_lessons) -1].position + 1
    else:
        position = 1

    l, created = Lesson.objects.get_or_create(name=name,
                                              owner=owner,
                                              course=course,
                                              position=position)
    l.save()
    return l


def add_question(name, owner, lesson, testFile, description):

    # get other questions in this lesson
    lesson_questions = Question.objects.filter(lesson=lesson).order_by('position')

    # work out next position available
    if len(lesson_questions) > 0:
        position = lesson_questions[len(lesson_questions) -1].position + 1
    else:
        position = 1

    q, created = Question.objects.get_or_create(name=name,
                                                owner=owner,
                                                lesson=lesson,
                                                testFile=testFile,
                                                description=description,
                                                position=position,
                                                solved=True)
    q.save()
    return q


def add_file(question, name, contents):
    f, created = File.objects.get_or_create(question=question, name=name, contents=contents)
    f.save()
    return f


# function to return details of question files
def readQuestionFiles(questionDir):

    # define return format
    fileDetails = {
        'questionFiles': [],
        'testFile': {}
    }

    # loop through dir
    for file in os.listdir(questionDir):

        # add all .java files excluding "Tests.java"
        if (file != "Tests.java") and file.endswith(".java"):
            fileDetails['questionFiles'].append(
                {'name': file,
                 'contents': readFile(file, questionDir)}
            )
        # add "Tests.java"
        elif (file == "Tests.java"):
            fileDetails['testFile'] = {'name': file,
                 'contents': readFile(file, questionDir)
            }

    # check files have been read
    if (fileDetails['questionFiles'] == [] or fileDetails['testFile'] == {}):
        return None

    return fileDetails


# method to get list of dir names in a parent dir
def getFolderNames(parentDir):

    dirList = []

    # loop through dir
    for file in os.listdir(parentDir):
        dirList.append(file)

    return dirList


def readFile(fileName, questionDir):

    filePath = os.path.join(questionDir, fileName)

    with open(filePath, 'r') as file:
        data = file.read()
    return data


if __name__ == '__main__':
    populate()