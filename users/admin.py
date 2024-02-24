from django.contrib import admin
from .models import User,StudentProfile,Skills,Education,Recruiter

admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(Skills)
admin.site.register(Education)
admin.site.register(Recruiter)