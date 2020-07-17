from django.db import models
from django.template.defaultfilters import slugify


# Model to store question data
class Question(models.Model):

    # question name
    name = models.CharField(max_length=128)

    # test file (contents)
    testFile = models.TextField(default=None)

    # slug for urls
    slug = models.SlugField(default=None, unique=True)

    # update the slug whenever Quesiton is created/changed
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Question, self).save(*args, **kwargs)

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


# Model to represent a question submission
class Submission(models.Model):

    # associated question
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.question.name

# Model to represent a file submitted as part of a submission
class SubmissionFile(models.Model):

    # associated submission
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, default=None, null=True)

    # file name
    name = models.CharField(max_length=32)

    # files contents as string
    contents = models.TextField()

    def __str__(self):
        return self.name
