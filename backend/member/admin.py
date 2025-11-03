from django.contrib import admin
from .models import Member, CoachMemberRelationship, FoodPost, FoodPostComment

# Register your models here.
admin.site.register(Member)
admin.site.register(CoachMemberRelationship)
admin.site.register(FoodPost)
admin.site.register(FoodPostComment)
