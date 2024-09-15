from django import forms
from users.models import CustomUser, UserProfile
from journalist.models import Article
from django.contrib.auth import get_user_model
from django.utils import timezone

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['role']

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'username', 'is_active', 'is_journalist', 'is_editor', 'is_head']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'type': 'email'})
        self.fields['username'].widget = forms.TextInput(attrs={'readonly': 'readonly'})

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'subtitle',
            'content',
            'author_name',  # You may not need this in the form
            'email',        # You may not need this in the form
            'image',
            'tags',
            'category',
            'publish_date',
            'agree_terms',
        ]

    def clean_publish_date(self):
        publish_date = self.cleaned_data['publish_date']
        if publish_date <= timezone.now().date():
            raise forms.ValidationError("Publish date must be in the future.")
        return publish_date

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise forms.ValidationError("Title must be at least 10 characters long.")
        return title

    def clean_email(self):
        email = self.cleaned_data['email']
        if not forms.EmailField().clean(email):
            raise forms.ValidationError("Enter a valid email address.")
        return email

