from django.contrib import admin
from question.models import Question, File, Submission, SubmissionFile

class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Question, QuestionAdmin)
admin.site.register(File)
admin.site.register(Submission)
admin.site.register(SubmissionFile)