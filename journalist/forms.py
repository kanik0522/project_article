from datetime import timezone
from django import forms
from .models import Article, Tag,Comment,Category
from django.utils import timezone

class ArticleStep1Form(forms.Form):
    title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))  # Adding the email field

    def __init__(self, *args, **kwargs):
        user_email = kwargs.pop('user_email', None)  # Pop the email from the keyword arguments
        super().__init__(*args, **kwargs)
        if user_email:
            self.fields['email'].initial = user_email

CATEGORY_CHOICES = [
    ('news', 'News'),
    ('opinion', 'Opinion'),
    ('feature', 'Feature'),
]

TAG_CHOICES = [
    ('politics', 'Politics'),
    ('sports', 'Sports'),
    ('tech', 'Tech'),
]


class ArticleStep2Form(forms.Form):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    category = forms.ChoiceField(
        choices=[(cat.id, cat.name) for cat in Category.objects.all()],
        widget=forms.Select
    )
    publish_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2024, 2031)),
        required=True
    )
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'})
        }
