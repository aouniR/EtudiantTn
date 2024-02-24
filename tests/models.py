from django.db import models
from users.models import StudentProfile
from django.core.exceptions import ValidationError
import hashlib
from django.utils import timezone

def validate_positive(value):
    if value <= 0:
        raise ValidationError("duration must be greater than 0.")

class TestOffer(models.Model):
    title = models.CharField(max_length=100)
    total_duration = models.PositiveIntegerField(editable=False)
    total_questions_number = models.PositiveIntegerField(default=0,editable=False)
    attempted = models.PositiveIntegerField(default=0,editable=False)
    success_rate = models.FloatField(default=0,editable=False)
    description = models.TextField(default="No Description")

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.total_duration = 0
            self.attempted = 0
            self.success_rate = 0
        super(TestOffer, self).save(*args, **kwargs)

    def update_total_duration(self):
        self.total_duration = sum(task.question_duration for task in self.questions.all())
        self.save()

    def __str__(self):
        return self.title

class MCQTask(models.Model):
    test = models.ForeignKey(TestOffer, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    right_answer = models.TextField(blank=True)
    question_duration = models.PositiveIntegerField(default=1, validators=[validate_positive])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.test.update_total_duration()

class Answers(models.Model):
    related_task = models.ForeignKey(MCQTask,on_delete=models.CASCADE,related_name='mcq_task_answer')
    other_answer = models.TextField()

class Session(models.Model):
    test = models.ForeignKey(TestOffer, on_delete=models.CASCADE, related_name='test_session')
    key = models.CharField(max_length=64,editable=False)
    start_time = models.DateTimeField(auto_now_add=True,editable=False)
    period = models.PositiveIntegerField(default=0,editable=False)
    
    def save(self, *args, **kwargs):
        self.key = hashlib.sha256((self.test.title+str(self.start_time)).encode()).hexdigest()
        super().save(*args, **kwargs)
    def update_period(self):
        end_time = timezone.now()
        time_difference = end_time - self.start_time
        self.period = time_difference.total_seconds()
        self.save()


class CandidateAnswer(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='candidate_answer', default=None)
    question = models.ForeignKey(MCQTask, on_delete=models.CASCADE, related_name='candidate_answer')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='exam_session',default=None)
    answer = models.TextField()
    is_correct = models.BooleanField(default=False,editable=False)

    def save(self, *args, **kwargs):
        if self.answer == self.question.right_answer:
            self.is_correct = True
        super(CandidateAnswer, self).save(*args, **kwargs)

class TestResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='test_results_student')
    test = models.ForeignKey(TestOffer, on_delete=models.CASCADE, related_name='test_results')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='test_results_session',default=None)
    score = models.PositiveIntegerField(editable=False)
    date_taken = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        total_questions = self.test.questions.count()
        if total_questions > 0:
            correct_answers = CandidateAnswer.objects.filter(question__test=self.test, is_correct=True,session=self.session).count()
            self.score = (correct_answers / total_questions) * 100
        else:
            self.score = 0

        self.test.attempted += 1
        if self.test.attempted > 0:
             self.test.success_rate = round((self.test.test_results.filter(score__gte=70).count() / self.test.attempted) * 100, 2)
        else:
            self.test.success_rate = 0
        self.test.save()
        super(TestResult, self).save(*args, **kwargs)
