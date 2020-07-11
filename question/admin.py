from django.contrib import admin
from question.models import Question, QuestionFiles, File

admin.site.register(Question)
admin.site.register(QuestionFiles)
admin.site.register(File)