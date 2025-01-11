from django import forms
from .models import UserTestimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = UserTestimonial
        fields = ['text', 'occupation']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Share your experience with us...',
                'rows': 5
            }),
            'occupation': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Your occupation'
            })
        }
        labels = {
            'text': 'Your Testimonial',
            'occupation': 'Your Occupation'
        }