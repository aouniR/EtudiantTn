from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def is_recruiter(user):
    return user.groups.filter(name='Recruiter').exists()

def is_student(user):
    return user.groups.filter(name='Student').exists()

permission_required_for_recruiter_profile = permission_required('users.view_recruiter_profile', raise_exception=True)

permission_required_for_student_profile = permission_required('users.view_student_profile', raise_exception=True)

def student_profile_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_student(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect("my_protected_view")
    return _wrapped_view

def split_traffic(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_student(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect("rec_dashboard")
    return _wrapped_view


def recruiter_profile_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if is_recruiter(request.user):
            return view_func(request, *args, **kwargs)
        else:
            return redirect("my_protected_view")
    return _wrapped_view
