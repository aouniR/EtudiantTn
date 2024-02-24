from django import forms
from django.core.validators import MinLengthValidator
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, Skills, Education, Recruiter

class UserCreationFormExtended(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'email', 'password1', 'password2', 'name', 'address', 'city', 'zip_code', 'phone']
        
class SkillsForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['skill_type', 'skill_name', 'level']

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['cycle_type', 'type_of_training', 'institution', 'field_of_study', 'period']

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['gender', 'age', 'cv_pdf', 'other_documents_pdf']


class CompleteStudentProfileForm(forms.ModelForm):
    skills = SkillsForm()
    educations = EducationForm()

    class Meta:
        model = StudentProfile
        fields = ['gender', 'age', 'cv_pdf', 'other_documents_pdf']


class RecruiterRegistrationForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea,
        validators=[MinLengthValidator(limit_value=5, message="Description should be at least 5 words.")],
        required=False
    )

    class Meta:
        model = Recruiter
        fields = ['description']
