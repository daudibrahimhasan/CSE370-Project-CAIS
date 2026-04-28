from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.db import connection
from django.shortcuts import redirect, render

from connect import dictfetchone


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, username, password, role, is_active
                FROM admin_auth_adminuser
                WHERE username = %s
                LIMIT 1
                """,
                [username],
            )
            user = dictfetchone(cursor)

        if user and user['is_active'] and check_password(password, user['password']):
            request.session['user_id'] = user['id']
            request.session['username'] = user['username']
            request.session['role'] = user.get('role') or 'Viewer'
            messages.success(request, f"You are now logged in as {username}.")
            return redirect('dashboard')

        messages.error(request, "Invalid username or password.")

    return render(request, 'admin_auth/login.html')


def admin_logout(request):
    request.session.flush()
    messages.info(request, "You have successfully logged out.")
    return redirect('home')
