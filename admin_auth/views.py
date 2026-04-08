from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are now logged in as {username}.")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'admin_auth/login.html', {'form': form})

def admin_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'admin_auth/login.html')

def dashboard(request):
    # This is the main dashboard for the new CAS UI
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    # Let's get some stats to pass to the dashboard
    from crimes.models import Crime
    from warrants.models import Warrant
    from cases.models import Case
    from criminals.models import Criminal
    from django.db.models import Count
    
    total_crimes = Crime.objects.count()
    active_warrants = Warrant.objects.filter(status='Active').count()
    open_cases = Case.objects.filter(status='Open').count()
    
    # Repeat offenders roughly > 2 (from previous logic)
    repeat_offenders_count = len(Criminal.objects.annotate(crime_count=Count('crimes_involved')).filter(crime_count__gte=2))

    context = {
        'total_crimes': total_crimes,
        'active_warrants': active_warrants,
        'open_cases': open_cases,
        'repeat_offenders_count': repeat_offenders_count
    }
    
    return render(request, 'dashboard.html', context)
