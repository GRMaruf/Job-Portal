from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app_base.models import *

class FormControlMixin():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for x in self.fields.values():
            x.widget.attrs['class'] = 'form-control'

class RegisterForm(FormControlMixin, UserCreationForm):
    class Meta:
        model = UserModel
        fields = [
            'username',
            'email',
            'user_type',
            'password1',
            'password2'
        ]
    

class LoginForm(FormControlMixin, AuthenticationForm):
    pass

class RecruiterForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = RecruiterModel
        fields = [
            'name',
            'address',
            'email'
        ]

class SeekerForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = SeekerModel
        fields = [
            'name',
            'bio',
            'email',
            'image',
        ]

class CategoryForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class SkillSetForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = SkillSet
        fields = ['name']

class JobPostForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            'title',
            'openings',
            'category',
            'description',
            'skill_set',
        ]
        
class ApplicationForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Applications
        fields = [
            'resume',
        ]


