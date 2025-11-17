from django.contrib import admin

from .models import WorkoutDay, WorkoutDayCompletion, WorkoutProgram, WorkoutAssignment

admin.site.register(WorkoutProgram)
admin.site.register(WorkoutDay)
admin.site.register(WorkoutDayCompletion)
admin.site.register(WorkoutAssignment)
