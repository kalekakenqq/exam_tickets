from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email', 'message']

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        if len(message) < 10:
            raise forms.ValidationError('сообщение слишком короткое (минимум 10 символов)')
        return message

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if '@' not in email:
            raise forms.ValidationError('введите корректный email')
        return email
