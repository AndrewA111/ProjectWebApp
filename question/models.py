from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


# Model to represent course (set of lessons)
class Course(models.Model):

    # course name (unique)
    name = models.CharField(max_length=128, unique=True)

    # Course owner/creator
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # slug for urls
    slug = models.SlugField(default=None, unique=True)

    # update the slug whenever Course is created/changed
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# Model to represent a lesson (set of questions)
class Lesson(models.Model):

    # question name
    name = models.CharField(max_length=128, unique=True)

    # Lesson owner/creator
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, unique=False)

    # course this lesson is a member of
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)

    # slug for urls
    slug = models.SlugField(default=None, unique=True)

    class Meta:
        # make lesson name unique for this course
        unique_together = ('name', 'course')

    # update the slug whenever Lesson is created/changed
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Lesson, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# Model to store question data
class Question(models.Model):

    # question name
    name = models.CharField(max_length=128, unique=True)

    # Question owner/creator
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # lesson this question is a member of
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)

    # test file (contents)
    testFile = models.TextField(default=None, null=True, blank=True)

    # textual description describing question
    description = models.TextField(default=None, null=True, blank=True)

    # boolean to indicate if author has successfull solved problem
    solved = models.BooleanField(default=False)

    # slug for urls
    slug = models.SlugField(default=None, unique=True)

    class Meta:
        # make question name unique for this lesson
        unique_together = ('name', 'lesson')

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


class UserProfile(models.Model):

    # link this profile to a User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # user bio
    bio = models.CharField(max_length=256, blank=True)

    def __str__(self):
        return self.user.username
