from django import forms
from .models import UserTestimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = UserTestimonial
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-input form-textarea',
                'placeholder': 'Share your experience with us...',
                'rows': 5
            })
        }
        labels = {
            'text': 'Your Testimonial'
        }
