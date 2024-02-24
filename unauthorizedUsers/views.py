from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from users.decorators import student_profile_only

@login_required
def my_protected_view(request):
    return render(request, 'unauthorizedUsers.html')

@login_required
@student_profile_only
def error_cand_view(request):
    err_msg = request.GET.get('err_msg', None)
    return render(request, 'error_cand.html',{'err_msg': err_msg})