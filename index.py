from django.shortcuts import redirect, render

from connect import is_logged_in, public_feature_context


def home(request):
    if is_logged_in(request):
        return redirect('dashboard')
    return render(request, 'admin_auth/features.html', public_feature_context())
