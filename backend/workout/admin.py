from django.contrib import admin

from .models import (
    WorkoutAssignment,
    WorkoutDay,
    WorkoutDayCompletion,
    WorkoutProgram,
)

admin.site.register(WorkoutProgram)
admin.site.register(WorkoutDay)
admin.site.register(WorkoutDayCompletion)
admin.site.register(WorkoutAssignment)
