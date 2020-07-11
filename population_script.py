import os
import project_web_app.settings
import pprint

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_web_app.settings')

import django
django.setup()

def populate():

    root = project_web_app.settings.BASE_DIR
    questions = os.path.join(root, 'questionFiles')

    # ArrayList question

    # folder
    arrayListFolder = os.path.join(questions, 'arrayList')

    arrayListDetails = readQuestionFiles(arrayListFolder)
    pprint.pprint(arrayListDetails)



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



def readFile(fileName, questionDir):

    filePath = os.path.join(questionDir, fileName)

    with open(filePath, 'r') as file:
        data = file.read()
    return data


if __name__ == '__main__':

    # test code to open files
    # root = project_web_app.settings.BASE_DIR
    # questions = os.path.join(root, 'questionFiles')
    # questionFolder = os.path.join(questions, 'calculator')
    # question = os.path.join(questionFolder, 'Calculator.java')
    # output = readFile(question)
    # print(output)

    populate()