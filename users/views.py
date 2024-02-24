from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login
from django.contrib import messages
from django.core.mail import send_mail
from .models import User
from .forms import UserCreationFormExtended, CompleteStudentProfileForm,RecruiterRegistrationForm

def register_student(request):
    if request.method == 'POST':
        user_form = UserCreationFormExtended(request.POST)
        student_profile_form = CompleteStudentProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and student_profile_form.is_valid():
            user = user_form.save()
            student_profile = student_profile_form.save(commit=False)
            student_profile.user = user
            student_profile.save()
            print("sending email of confirmation")
            send_mail(
                'Registration Confirmation',
                'Thank you for registering! Wait for our validation soon!',
                'freelance2020aouni@gmail.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'An email confirmation has been sent to your email address.')
            return redirect('registration_confirmation')
    else:
        user_form = UserCreationFormExtended()
        student_profile_form = CompleteStudentProfileForm()
    return render(request, 'registration/register_student.html', {'user_form': user_form, 'student_profile_form': student_profile_form})

def register_recruiter(request):
    if request.method == 'POST':
        user_form = UserCreationFormExtended(request.POST)
        recruiter_profile_form = RecruiterRegistrationForm(request.POST)
        if user_form.is_valid() and recruiter_profile_form.is_valid():
            user = user_form.save()
            recruiter_profile = recruiter_profile_form.save(commit=False)
            recruiter_profile.user = user
            recruiter_profile.save()
            print("sending email of confirmation")
            send_mail(
                'Registration Confirmation',
                'Thank you for registering! Wait for our validation soon!',
                'freelance2020aouni@gmail.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'An email confirmation has been sent to your email address.')
            return redirect('registration_confirmation')
        else:
            messages.error(request, 'Form validation failed.')
            print(recruiter_profile_form.errors)
    else:
        user_form = UserCreationFormExtended()
        recruiter_profile_form = RecruiterRegistrationForm()

    return render(request, 'registration/register_recruiter.html', {'user_form': user_form, 'recruiter_profile_form': recruiter_profile_form})

def registration_confirmation(request):
    return render(request, 'registration/registration_confirmation.html')

def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user and user.check_password(password):
            login(request, user)  
            next_url = request.GET.get('next')
            if next_url :
                return redirect(next_url)
            else:
                return redirect('dashboard')
        else:
            context={
                'error_msg':'Invalid email or password.'
            }
            print(context)
            return render(request,'login.html',context)
    return render (request, 'login.html')   

def register(request):
    return render(request, 'registration/register.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'logout.html')