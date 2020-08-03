from django.forms import Textarea
from django.db import models
from django import forms
from django.forms import formset_factory
from question.models import SubmissionFile, Submission


# Form for submitting a file
class SubmissionFileForm(forms.ModelForm):

    # submission this file is associated with
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, default=None, null=True)

    # file name
    name = forms.CharField(widget=forms.HiddenInput(), max_length=32)

    # file contents
    contents = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 100%; height: 80vh', 'rows': '20'}))

    class Meta:
        model = SubmissionFile
        exclude = ('submission',)


# Form for uploading a file
class UploadFileForm(forms.Form):

    # file name
    name = forms.CharField(max_length=32)

    # file contents
    contents = forms.CharField(widget=forms.Textarea())


class UploadForm(forms.Form):

    question_name = forms.CharField(max_length=32);

    question_description = forms.CharField(max_length=128)

    test_file = forms.CharField(widget=forms.Textarea)