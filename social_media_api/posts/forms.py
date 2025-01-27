from django import forms
from .models import Post, Comment

from django.forms.widgets import SelectDateWidget
# markdown form fields
from martor.fields import MartorFormField


class PostForm(forms.ModelForm):
    content = MartorFormField()

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


'''enable date selection widgets fora more user friendly date range selection'''


class DateForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
