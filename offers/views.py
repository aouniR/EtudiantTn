from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import student_profile_only
from .models import Offer

@login_required
@student_profile_only
def offer_list(request):
    all_offers = Offer.objects.all()
    internships = all_offers.filter(offer_type="Internship")
    offers = all_offers.exclude(offer_type="Internship")
    return render(request, 'offer/offer_list.html', {'offers': offers,'internships':internships})
