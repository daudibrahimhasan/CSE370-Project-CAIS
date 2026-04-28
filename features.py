from django.shortcuts import render

from connect import public_feature_context


def features_page(request):
    return render(request, 'admin_auth/features.html', public_feature_context())
