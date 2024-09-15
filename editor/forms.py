from datetime import timezone
from django import forms
from journalist.models import Article
from editor.models import Review


class ArticleReviewForm(forms.ModelForm):
    approved = forms.BooleanField(required=False, label='Approve this article')
    rejected = forms.BooleanField(required=False, label='Reject this article')

    class Meta:
        model = Review
        fields = ['approved', 'rejected']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget = forms.CheckboxSelectMultiple()
        self.fields['publish_date'].widget = forms.DateInput(attrs={'type': 'date'})

    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')
        if publish_date <= timezone.now().date():
            raise forms.ValidationError('Publish date must be in the future.')
        return publish_date

    def clean(self):
        cleaned_data = super().clean()
        approved = cleaned_data.get('approved')
        rejected = cleaned_data.get('rejected')

        # Ensure only one of 'approved' or 'rejected' is selected
        if approved and rejected:
            raise forms.ValidationError('An article cannot be both approved and rejected. Please choose one.')
        
        return cleaned_data