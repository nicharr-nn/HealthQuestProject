from django.db import models

class User(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
        ('normal user', 'Normal User'), # ('trainee', 'Trainee'),
        ('member', 'Member'),
        ('coach', 'Coach'),
    ]
    
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='normal user')
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     return self.username