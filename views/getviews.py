from django.shortcuts import render, redirect, reverse
from apps.dashboard_app.models import User
from django.contrib import messages
from .functions import *

def index(request):
    if loggedIn(request):
        return redirect(dashboard)
    else:
        return render(request, "dashboard_app/index.html")

def login(request):
    return render(request, "dashboard_app/login.html")

def register(request):
    return render(request, "dashboard_app/register.html")

def dashboard(request):
    if loggedIn(request):
        context = {
            'loggedIn': True,
            'users':    User.objects.all(),
        }

        # admins get redirected to admin dashboard
        if User.objects.get(id=request.session['id']).level.level == 'admin':
            return redirect(admin_dashboard)
        return render(request, 'dashboard_app/dashboard.html', context)

    else:
        messages.error(request, "Must be logged in to view dashboard")
        return redirect(login)

def show_one(request, id):
    if loggedIn(request):

        # admins will have an edit button for other users
        admin = False
        if User.objects.get(id=request.session['id']).level.level == 'admin':
            admin = True

        context = {
            'user':     User.objects.get(id=id),
            'admin':    admin,
            'posts':    User.objects.get(id=id).recieved_posts.all(),
            'loggedIn': loggedIn(request),
        }
        return render(request, 'dashboard_app/show_one.html', context)

    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)

def edit(request):
    if loggedIn:
        context = {
            'user':     User.objects.get(id=request.session['id']),
            'loggedIn': True,
        }
        return render(request, 'dashboard_app/edit.html', context)
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)

def admin_edit(request, id):
    if not loggedIn(request):
        messages.error(request, "You must be logged in to do that")
        return redirect(login)
    else:
        edit_user    = User.objects.get(id=id)
        current_user = User.objects.get(id=request.session['id'])

        # if trying to edit own profile, go to regular edit page
        if edit_user == current_user:
            return redirect(edit)

        # only admins can edit other profiles
        elif current_user.level.level != 'admin':
            messages.error(request, "You must have admin priviledges to do that")
            return redirect(dashboard)
        else:
            context = {
                'user': edit_user,
                'loggedIn': True
            }
            return render(request, 'dashboard_app/admin_edit.html', context)

def admin_dashboard(request):
    if loggedIn(request):
        if User.objects.get(id=request.session['id']).level.level != 'admin':
            messages.error(request, "You must be an admin to do that")
        else:
            context = {
                'loggedIn': True,
                'users': User.objects.all(),
            }
            return render(request, 'dashboard_app/admin_dashboard.html', context)
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)

def new_user(request):
    if loggedIn(request):
        if User.objects.get(id=request.session['id']).level.level != 'admin':
            messages.error(request, "You must be an admin to do that")
            return redirect(dashboard)
        else:
            return render(request, 'dashboard_app/new_user.html')
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)
