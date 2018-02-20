from django.shortcuts import redirect
from apps.dashboard_app.models import User, Level, Post, Comment
from django.contrib import messages
import bcrypt
from .functions import *
from .getviews import *

def create(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect(register)

    else:
        messages.success(request, "Successfully created new user " + request.POST['first_name'] + "!")
        
        user = User.objects.create_user(request.POST)

        # Store current user info in session
        request.session['id']    = user.id
        request.session['name']  = user.first_name
        request.session['email'] = user.email

        return redirect(dashboard)

def login_submit(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, "No user could be found with that email address!")
        return redirect(login)

    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.success(request, "Successfully logged in, welcome " + user.first_name + "!")

        # on successfull login, store user info in session
        request.session['id']    = user.id
        request.session['name']  = user.first_name
        request.session['email'] = user.email

        return redirect(dashboard)
    else:
        messages.error(request, "Wrong password, try again")
        return redirect(login)

def logout_user(request):
    logout(request)
    return redirect(index)

def update(request):
    if loggedIn(request):
        user = User.objects.get(id=request.session['id'])

        errors = User.objects.validate_profile(request.POST, user.email)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(edit)

        user.first_name = request.POST['first_name']
        user.last_name  = request.POST['last_name']
        user.email      = request.POST['email']

        user.save()
        messages.success(request, "Profile updated successfully")

        return redirect(show_one, id=user.id)
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)

def update_pw(request):
    if loggedIn(request):
        user   = User.objects.get(id=request.session['id'])
        errors = User.objects.validate_password(request.POST, user.password)

        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(edit)

        user.password = bcrypt.hashpw(request.POST['password_new'].encode(), bcrypt.gensalt())

        user.save()
        messages.success(request, "Password has been updated successfully")

        return redirect(show_one, id=user.id)
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)


def admin_update(request, id):
    if loggedIn(request):
        user = User.objects.get(id=id)
        
        errors = User.objects.validate_profile(request.POST, user.email)
        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(admin_edit, id=id)

        user.first_name = request.POST['first_name']
        user.last_name  = request.POST['last_name']
        user.email      = request.POST['email']

        user_level = request.POST['level']
        level      = Level.objects.get(level=user_level)
        user.level = level

        user.save()

        messages.success(request, "User updated successfully")
        return redirect(show_one, id=user.id)
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)

def admin_update_pw(request, id):
    if loggedIn(request):
        user = User.objects.get(id=id)
        errors = User.objects.admin_validate_pw(request.POST)

        if errors:
            for error in errors:
                messages.error(request, errors[error])
            return redirect(admin_edit, id=user.id)

        user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        user.save()
        messages.success(request, "Password has been updated successfully")

        return redirect(show_one, user.id)
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)

def update_desc(request):
    if loggedIn(request):
        user = User.objects.get(id=request.session['id'])
        user.desc = request.POST['desc']
        user.save()

        messages.success(request, "User description has been updated successfully")

        return redirect(show_one, id=user.id)
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)

def create_post(request, id):
    if loggedIn(request):
        poster    = User.objects.get(id=request.session['id'])
        recipient = User.objects.get(id=id)
        post      = Post.objects.create(content=request.POST['message'], poster=poster, recipient=recipient)

        messages.success(request, "Post was made successfully")

        return redirect(show_one, id=id)
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)

def create_comment(request, user_id, post_id):
    if loggedIn(request):
        poster    = User.objects.get(id=request.session['id'])
        recipient = User.objects.get(id=user_id)
        post      = Post.objects.get(id=post_id)
        comment   = Comment.objects.create(content=request.POST['comment'], poster=poster, recipient=recipient, post=post)

        post.has_comments = True
        post.save()

        messages.success(request, "Comment successfully saved")

        return redirect(show_one, id=user_id)
    else:
        messages.error(request, "You must be logged in to do that")
        return redirect(login)

def delete(request, id):
    if not loggedIn(request):
        messages.error(request, "You must be logged in to do that")
        return redirect(login)
    else:
        current_user = User.objects.get(id=request.session['id'])
        delete_user  = User.objects.get(id=id)
        if current_user.level.level == 'admin':

            # if an admin is removing an admin, check to see if there's at least one left
            if delete_user.level.level == 'admin':
                if len(Level.objects.filter(level='admin')) < 2:
                    messages.error(request, "Cannot delete the last admin!!")
                    return redirect(dashboard)
            else:
                User.objects.get(id=id).delete()
                messages.success(request, "User " + id + " has been successfully deleted")

                # log out if deleting self
                if current_user == delete_user:
                    logout(request)
                    return redirect(index)
                else:
                    return redirect(dashboard)
        else:

            # normal users can't delete anyone but themselves
            if current_user != delete_user:
                messages.error(request, "You must have admin priviledges to do that")
                return redirect(dashboard)
            else:
                logout(request)
                current_user.delete()
                messages.success(request, "Your user has been successfully deleted")
                return redirect(index)

def create_user(request):
    errors = User.objects.validator(request.POST)
    if errors:
        for error in errors:
            messages.error(request, errors[error])
        return redirect(register)

    else:
        messages.success(request, "Successfully created new user " + request.POST['first_name'] + "!")
        
        user = User.objects.create_user(request.POST)

        return redirect(dashboard)
