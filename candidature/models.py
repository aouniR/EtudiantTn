from django.db import models
from offers.models import Offer  
from users.models import StudentProfile

class Candidature(models.Model):
    STATE_CHOICES = [
        ('En_cours', 'En cours'),
        ('Vu', 'Vu'),
        ('Preselectionné', 'Préselectionné'),
        ('Cloturé', 'Cloturé')
    ]
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE,related_name="candidat")
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE,related_name="offer")
    submitted_date = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='En_cours')

    def __str__(self):
        return f"{self.student_profile.user.name} - {self.offer.title}"
    
