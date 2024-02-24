from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.decorators import student_profile_only
from .models import RentOffer

@login_required
@student_profile_only
def rent_offers(request):
    rent_offers_all = RentOffer.objects.all()
    context = {
        'rent_offers_all': rent_offers_all,
    }

    return render(request, 'rent_offers_main.html', context)