from django.contrib import admin
from question.models import Question, File

class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Question, QuestionAdmin)
admin.site.register(File)