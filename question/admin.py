from django.contrib import admin
from question.models import Question, File, Submission, SubmissionFile, UserProfile, Course, Lesson, Bookmark


class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(File)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(SubmissionFile)
admin.site.register(UserProfile)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Bookmark)