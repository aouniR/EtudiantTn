from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from users.decorators import student_profile_only
from .models import Candidature
from offers.models import Offer

@login_required
@student_profile_only
def save_candidature(request, pk):
    student_profile = request.user.student_profile
    offer = get_object_or_404(Offer, pk=pk)
    existing_candidature = Candidature.objects.filter(student_profile=student_profile, offer=offer).first()

    if existing_candidature:
        print(existing_candidature)
        print(offer)
        err_msg = "existing_candidature"
        error_url = reverse('error_cand') + f'?err_msg={err_msg}'
        return  redirect(error_url)

    if student_profile is not None:
        Candidature.objects.create(
            student_profile=student_profile,
            offer=offer,
        )
        return redirect('dashboard')
    else:
        return  redirect('error_cand')
