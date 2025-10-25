from django.contrib import admin
from .models import Member, CoachMemberRelationship

# Register your models here.
admin.site.register(Member)
admin.site.register(CoachMemberRelationship)
