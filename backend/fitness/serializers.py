
from rest_framework import serializers
from django.contrib.auth.models import User
from django.apps import apps

def get_fitness_goal_model():
    return apps.get_model("fitness", "FitnessGoal")

class FitnessGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_fitness_goal_model()
        fields = ["id", "goal_type", "start_date", "end_date"]
        read_only_fields = ["id", "start_date"]