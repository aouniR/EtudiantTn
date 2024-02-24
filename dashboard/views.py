from django.http import HttpResponse
from users.decorators import recruiter_profile_only, student_profile_only,split_traffic
from users.forms import EducationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import StudentProfile,Skills,Education,Recruiter
from tests.models import TestResult
from offers.models import Offer
from candidature.models import Candidature
from django.conf import settings
from cryptography.fernet import Fernet
from offers.forms import OfferForm

@login_required
@split_traffic
def dashboard(request):
    student_profile = request.user.student_profile
    candidatures = Candidature.objects.filter(student_profile=student_profile)
    candidature_count = candidatures.count()
    test_count = TestResult.objects.filter(student=student_profile).count()
    interviewed = candidatures.filter(state='Preselectionné').count()
    percent_interviewed =round((interviewed/candidature_count)*100, 2) if candidature_count>1 else 0 
    context = {'candidature_count': candidature_count,
               'candidatures': candidatures,
               'test_count': test_count,
               'percent_interviewed':percent_interviewed
               }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
@recruiter_profile_only
def rec_dashboard(request):
    recruiter = get_object_or_404(Recruiter, user=request.user)
    offers = Offer.objects.filter(recruiter=recruiter)
    liste_candidate = [list(Candidature.objects.filter(offer=offer).select_related('student_profile')) for offer in offers]
    nbre_candidature = [Candidature.objects.filter(offer=offer).count() for offer in offers]

    context = {
        'offers': offers,
        'liste_candidate':liste_candidate,
        'nbre_candidature':nbre_candidature
    }
    return render(request, 'dashboard/rec_dashboard.html', context)

@login_required
@student_profile_only
def Cv(request):
    studentprofile = get_object_or_404(StudentProfile, user=request.user)
    skills = Skills.objects.filter(student_profile_id=studentprofile.pk)
    educations = Education.objects.filter(student_profile_id=studentprofile.pk)
    EForm = EducationForm()
    CV = studentprofile.retrieve_pdf(studentprofile.cv_pdf)
    OtherDoc = studentprofile.retrieve_pdf(studentprofile.other_documents_pdf)
    context ={
        'studentprofile': studentprofile, 
        'skills': skills,'EForm':EForm,
        'educations':educations,
        'CV':CV,
        'OtherDoc':OtherDoc
    }
    return render(request, 'Cv/Cv.html', context)

@login_required
@student_profile_only
def Tests(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    user_test_results = TestResult.objects.filter(student=student_profile)
    return render(request, 'Tests/tests.html', {'user_test_results': user_test_results})

@login_required
@student_profile_only
def Candidatures(request):
    return render(request, 'Candidatures/Candidatures.html')

@login_required
@student_profile_only
def Messages(request):
    return render(request, 'Messages/Messages.html')

@login_required
@student_profile_only
def save_Cv_pdf(request):
    if request.method == 'POST':
        new_cv_pdf_file = request.FILES.get('new_cv_pdf')
        student_profile = get_object_or_404(StudentProfile, user=request.user)
        student_profile.delete_pdf(student_profile.cv_pdf)
        student_profile.cv_pdf = new_cv_pdf_file
        student_profile.saveCV()
        return redirect('Cv') 
    return render(request, 'Cv/Cv.html')  

@login_required
@student_profile_only
def downloadCV(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    decrypted_content=student_profile.DowloadCV()
    if decrypted_content:
        response = HttpResponse(decrypted_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="CV.pdf"'
        return response
    return redirect('Cv')


@login_required
@student_profile_only
def save_Other_Docs_pdf(request):
    if request.method == 'POST':
        new_Other_Docs_pdf_file = request.FILES.get('new_Other_Docs_pdf')
        student_profile = StudentProfile.objects.get(user=request.user)
        student_profile.other_documents_pdf = new_Other_Docs_pdf_file
        student_profile.saveOtherDoc()
        return redirect('Cv') 
    return render(request, 'Cv/Cv.html')  

@login_required
@student_profile_only
def downloadOtherDoc(request):
    student_profile = request.user.student_profile
    cv_pdf_encrypted_path = student_profile.other_documents_pdf.path
    if cv_pdf_encrypted_path:
        encryption_key = settings.ENCRYPTION_KEY
        cipher_suite = Fernet(encryption_key)
        with open(cv_pdf_encrypted_path, 'rb') as file:
            file_content = file.read()
            decrypted_content = cipher_suite.decrypt(file_content)
        response = HttpResponse(decrypted_content, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="other_documents_pdf.pdf"'
        return response
    else:
        return render(request, 'Cv/Cv.html')

@login_required
@student_profile_only
def save_photo(request):
    if request.method == 'POST':
        new_photo_file = request.FILES.get('new_Photo')
        request.user.profile_picture = new_photo_file
        request.user.save()
        return redirect('Cv') 
    return render(request, 'Cv/Cv.html')

@login_required
@student_profile_only
def save_skills(request):
    if request.method == 'POST':
        studentprofile = get_object_or_404(StudentProfile, user=request.user)
        new_skill_name = request.POST.get('new_skill_name')
        new_level = request.POST.get('new_level')
        if new_skill_name and new_level:
            new_skill = Skills(student_profile=studentprofile, skill_name=new_skill_name, level=new_level)
            new_skill.save()
        return redirect('Cv')
     
@login_required
@student_profile_only    
def delete_skill(request, skill_id):
    studentprofile = get_object_or_404(StudentProfile, user=request.user)
    skills = Skills.objects.filter(student_profile_id=studentprofile.pk)
    skill = get_object_or_404(skills, id=skill_id)
    skill.delete()
    return redirect('Cv') 

@login_required
@student_profile_only
def save_education(request):
    if request.method == 'POST':
        studentprofile = get_object_or_404(StudentProfile, user=request.user)
        cycle_type = request.POST.get('cycle_type')
        type_of_training = request.POST.get('type_of_training')
        institution = request.POST.get('institution')
        field_of_study = request.POST.get('field_of_study')
        period = request.POST.get('period')
        
        if cycle_type and type_of_training and institution and field_of_study and period:
            new_education = Education(
                student_profile=studentprofile,
                cycle_type=cycle_type,
                type_of_training=type_of_training,
                institution=institution,
                field_of_study=field_of_study,
                period=period
            )
            new_education.save()

        return redirect('Cv')

@login_required    
@student_profile_only
def delete_education(request, education_id):
    studentprofile = get_object_or_404(StudentProfile, user=request.user)
    educations = Education.objects.filter(student_profile_id=studentprofile.pk)
    education = get_object_or_404(educations, id=education_id)
    education.delete()
    return redirect('Cv') 

@login_required    
@recruiter_profile_only
def add_offer(request):
    if request.method == 'POST':
        recruiter = get_object_or_404(Recruiter, user=request.user)
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        level = request.POST.get('level')
        salary = request.POST.get('salary')
        offer_type = request.POST.get('offer_type')
        period= request.POST.get('period')
        description = request.POST.get('description')
        if recruiter and title and company and location and level and salary and offer_type and period and description:
            new_offer = Offer(
                recruiter = recruiter ,
                title = title,
                company = company,
                location = location,
                level = level,
                salary = salary,
                offer_type = offer_type,
                period= period,
                description = description
            )
            new_offer.save()
            return redirect('rec_dashboard')  
    else:
        form = OfferForm()
    return render(request, 'add_offers/add_offer.html', {'form': form})