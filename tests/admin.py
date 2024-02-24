from django.contrib import admin
from .models import TestOffer,MCQTask,Answers,CandidateAnswer,TestResult,Session

admin.site.register(TestOffer)
admin.site.register(MCQTask)
admin.site.register(Answers)
admin.site.register(CandidateAnswer)
admin.site.register(TestResult)
admin.site.register(Session)
