from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if User.objects.filter(email=postData['email']):
            errors['usedEmail'] = "Email address already in use"
        if len(postData['password']) < 8:
            errors['pwlength'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['password_confirm']:
            errors['pw'] = "Password didn't match"
        if (len(postData['first_name']) < 1 or len(postData['last_name']) < 1):
            errors['name'] = "First and last names must not be empty"
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Must be a valid email address"
        return errors

    def validate_profile(self, postData, email):
        errors = {}
        if email != postData['email']:
            if User.objects.filter(email=postData['email']):
                errors['usedEmail'] = "Email address already in use"
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Must be a valid email address"
        if (len(postData['first_name']) < 1 or len(postData['last_name']) < 1):
            errors['name'] = "First and last names must not be empty"
        return errors

    def validate_password(self, postData, user_pw):
        errors = {}
        if not bcrypt.checkpw(postData['password_current'].encode(), user_pw.encode()):
            errors['wrong_pw'] = "Current password didn't match, try again"
        elif postData['password_new'] != postData['password_confirm']:
            errors['bad_pw_match'] = "New password and confirmed password didn't match"
        if len(postData['password_new']) < 8:
            errors['pw_length'] = "Password must be at least 8 characters"
        return errors

    def admin_validate_pw(self, postData):
        errors = {}
        if len(postData['password']) < 8:
            errors['pwlength'] = "Password must be at least 8 characters"
        elif postData['password'] != postData['password_confirm']:
            errors['pw'] = "Password didn't match"
        return errors

    def create_user(self, postData):
        first_name = postData['first_name']
        last_name  = postData['last_name']
        email      = postData['email']
        password   = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        
        if len(self.all()) == 0:
            level = 'admin'
            if not Level.objects.filter(level='admin'):
                Level.objects.create(level='admin')
        else:
            level = 'user'
            if not Level.objects.filter(level='user'):
                Level.objects.create(level='user')

        user = self.create(first_name=first_name, last_name=last_name, email=email, password=password, level=Level.objects.get(level=level))
        return user

class Level(models.Model):
    level      = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name  = models.CharField(max_length=255)
    email      = models.CharField(max_length=255)
    password   = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    level      = models.ForeignKey(Level, related_name='users')
    desc       = models.CharField(max_length=255)

    objects = UserManager()

class Post(models.Model):
    content      = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
    poster       = models.ForeignKey(User, related_name="posts")
    recipient    = models.ForeignKey(User, related_name="recieved_posts")
    has_comments = models.BooleanField(default=False)

class Comment(models.Model):
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    poster     = models.ForeignKey(User, related_name="comments")
    recipient  = models.ForeignKey(User, related_name="recieved_comments")
    post       = models.ForeignKey(Post, related_name="comments")

