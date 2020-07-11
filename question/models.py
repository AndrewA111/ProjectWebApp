from django.db import models


# Model to store question data
class Question(models.Model):
    name = models.CharField(max_length=128)
    testFile = models.TextField()

    def __str__(self):
        return self.name


# Model to store files associated with a question
class QuestionFiles(models.Model):

    # Associated Question object
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


# Model to store file (name and contents, both as strings)
class File(models.Model):

    # associated set of QuestionFiles
    questionFile = models.ForeignKey(QuestionFiles, on_delete=models.CASCADE)

    # file name
    name=models.CharField(max_length=32)

    # files contents as string
    contents=models.TextField()

