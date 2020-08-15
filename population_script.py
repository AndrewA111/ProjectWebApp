import os

from django.contrib.auth import get_user_model

import project_web_app.settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_web_app.settings')

import django
django.setup()

import pprint
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from question.models import File, Question
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

    tutor_user = User.objects.create_user(username='john', email="j@a.com", password="HelloWorld123")
    tutor_user.groups.add(create_group)

    root = project_web_app.settings.BASE_DIR
    questions = os.path.join(root, 'questionFiles')

    # loop through directories containing questions
    for questionDir in getQuestions(questions):

        # get question dir path
        questionPath = os.path.join(questions, questionDir)

        # read relevant files from dir
        questionDetails = readQuestionFiles(questionPath)

        # pretty print data for debugging
        # pprint.pprint(questionDetails)

        # get description
        description = readFile("Description.txt", questionPath)

        # make question
        question = add_question(questionDir, questionDetails['testFile']['contents'], description)

        # loop through files and create file objects
        for file in questionDetails['questionFiles']:
            add_file(question, file['name'], file['contents'])


def add_question(name, testFile, description):
    q, created = Question.objects.get_or_create(name=name,
                                                testFile=testFile,
                                                description=description,
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


# method to get list of question folders given the containing dir
def getQuestions(questionsDir):

    dirList = []

    # loop through dir
    for file in os.listdir(questionsDir):
        dirList.append(file)

    return dirList


def readFile(fileName, questionDir):

    filePath = os.path.join(questionDir, fileName)

    with open(filePath, 'r') as file:
        data = file.read()
    return data


if __name__ == '__main__':
    populate()