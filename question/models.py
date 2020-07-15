from django.db import models


# Model to store question data
class Question(models.Model):
    name = models.CharField(max_length=128)
    testFile = models.TextField(default=None)

    def __str__(self):
        return self.name


# Model to store file (name and contents, both as strings)
class File(models.Model):

    # associated quesiton
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)

    # file name
    name = models.CharField(max_length=32)

    # files contents as string
    contents = models.TextField()

    def __str__(self):
        return self.name


class Submission(models.Model):

    # associated question
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.question.name


class SubmissionFile(models.Model):

    # associated submission
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, default=None)

    # file name
    name = models.CharField(max_length=32)

    # files contents as string
    contents = models.TextField()

    def __str__(self):
        return self.name
