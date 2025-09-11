from django.db import models

class FitnessGoal(models.Model):
    goal_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    goal_type = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    # def __str__(self):
    #     return f"Goal {self.goal_id} for User {self.user_id}"
