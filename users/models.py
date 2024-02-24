import os
from django.core.validators import MaxValueValidator
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser
from django.forms import ValidationError
from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings

class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    zip_code = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=25)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] 
    
    def save(self, *args, **kwargs):
        self.username=self.email
        super(User, self).save(*args, **kwargs)


class StudentProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    user= models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    gender = models.CharField(max_length=20,choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()

    cv_pdf = models.FileField(upload_to='cv_pdfs/')
    other_documents_pdf = models.FileField(upload_to='other_documents_pdfs/')
    skills = models.ManyToManyField('Skills', blank=True, related_name='student_profiles_custom')
    educations = models.ManyToManyField('Education', blank=True, related_name='student_profiles_custom')
    
    def saveCV(self, *args, **kwargs):
        if self.cv_pdf:
            self.encrypt_file(self.cv_pdf)
        super().save(*args, **kwargs)

    def saveOtherDoc(self, *args, **kwargs):
        if self.other_documents_pdf:
            self.encrypt_file(self.other_documents_pdf)
        super().save(*args, **kwargs)

    def delete_pdf(self,file_field):
        if self.retrieve_pdf(file_field):
            try:
                os.remove(file_field.path)
                print(f"File '{file_field.path}' deleted successfully.")
            except Exception as e:
                print(f"An error occurred while trying to delete the file: {e}")
                return None
        else:
            print("No PDF document found")
            return None
    
    def DowloadCV(self):
        return self.decrypt_file(self.cv_pdf) if self.retrieve_pdf(self.cv_pdf) else False

    def encrypt_file(self, file_field):
        encryption_key = settings.ENCRYPTION_KEY
        cipher_suite = Fernet(encryption_key)
        file_content = file_field.read()
        encrypted_content = cipher_suite.encrypt(file_content)
        file_field.save(file_field.name, ContentFile(encrypted_content), save=False)
    
    def decrypt_file(self, file_field):
        encryption_key = settings.ENCRYPTION_KEY
        cipher_suite = Fernet(encryption_key)

        with open(file_field.path, 'rb') as file:
            file_content = file.read()
        return cipher_suite.decrypt(file_content)
  
    def retrieve_pdf(self, file_field):
        return os.path.exists(file_field.path) if file_field else False
        
class Skills(models.Model):
    SKILL_TYPES = (
        ('IT', 'IT'),
        ('Language', 'Language'),
    )
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='skills_custom')
    skill_type = models.CharField(max_length=20,choices=SKILL_TYPES)
    skill_name = models.CharField(max_length=50)
    level = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(10)])

    def __str__(self):
        return f"{self.skill_type} - {self.skill_name} (Level: {self.level})"
    
class Education(models.Model):
    CYCLE_CHOICES = [
        ('secondary', 'Secondary'),
        ('higher_education', 'Higher Education'),
    ]
    TYPE_OF_TRAINING_CHOICES = [
        ('bac', 'Bac'),
        ('bac+3', 'Bac+3'),
        ('bac+5', 'Bac+5'),
        ('bac+8', 'Bac+8'),
    ]
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='educations_custom')
    cycle_type = models.CharField(max_length=20, choices=CYCLE_CHOICES)
    type_of_training = models.CharField(max_length=20, choices=TYPE_OF_TRAINING_CHOICES)
    institution = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    period = models.CharField(max_length=50)
    
class Recruiter(models.Model):
    def validate_min_length_50_words(value):
        words = value.split()
        if len(words) < 5:
            raise ValidationError('Description should be at least 5 words.')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='recruiter')
    description = models.TextField(validators=[validate_min_length_50_words])
