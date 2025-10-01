from django.contrib import admin
from .models import WorkoutProgram, WorkoutDay, WorkoutDayCompletion, WorkoutAssignment

admin.site.register(WorkoutProgram)
admin.site.register(WorkoutDay)
admin.site.register(WorkoutDayCompletion)
admin.site.register(WorkoutAssignment)