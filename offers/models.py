from django.db import models
from users.models import Recruiter
class Offer(models.Model):
    LEVEL_CHOICES = [
        ('Bac', 'Bac'),
        ('Bac+3', 'Bac+3'),
        ('Bac+5', 'Bac+5'),
    ]
    PERIOD_CHOICES= [
        ('CDD', 'CDD'),
        ('CDI', 'CDI'),
        ('Internship_period', 'internship_period'),
    ]
    TYPE_CHOICES= [
        ('Internship', 'intership'),
        ('Part-time Job', 'part_time_job'),
        ('Full-time Job', 'full_time_job'),
    ]
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    salary = models.PositiveIntegerField()
    offer_type = models.CharField(max_length=13, choices=TYPE_CHOICES)
    period= models.CharField(max_length=17, choices=PERIOD_CHOICES)
    description = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title

