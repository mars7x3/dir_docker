from django import forms

from dir.models import Resume, Review


class AddResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['status', 'category', 'title', 'price',
                  'description', 'phone', 'name', 'image', 'address']


class UpdateResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['id', 'status', 'category', 'title', 'price',
                  'description', 'phone', 'name', 'image', 'address']


class AddReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', ]

