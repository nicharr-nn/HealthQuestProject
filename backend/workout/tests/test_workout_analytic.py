from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.test import APIClient
from rest_framework import status
from workout.models import WorkoutDayCompletion, WorkoutProgram, WorkoutDay
from coach.models import Coach
from django.test import override_settings


User = get_user_model()
class AnalyticsTests(TestCase):
    """Tests for user analytics functionality"""

    def setUp(self):
        self.client = APIClient()

        # Create normal user
        self.normal_user = User.objects.create_user(
            username="normal_user", 
            password="pass123", 
            email="normal@example.com"
        )

        self.normal_profile = self.normal_user.userprofile
        self.normal_profile.role = "normal"
        self.normal_profile.save()
                # Create coach user
        self.coach_user = User.objects.create_user(
            username="coach", 
            password="coachpass",
            email="coach@example.com"
        )
        self.coach_profile = self.coach_user.userprofile
        self.coach_profile.role = "coach"
        self.coach_profile.save()

        # Create coach model instance
        self.coach = Coach.objects.create(
            user=self.coach_profile,
            public_id="C-00001",
            status_approval="approved"
        )

        # Create workout program
        self.program = WorkoutProgram.objects.create(
            coach=self.coach_profile,
            title="Test Program",
            description="Program for testing",
            difficulty_level="easy",
            duration=1,
            is_public=True,
            category="cardio"
        )

        # Create workout days
        self.workout_day_1 = WorkoutDay.objects.create(
            program=self.program,
            day_number=1,
            title="Day 1 - Test Workout",
            duration=45,
        )

        self.workout_day_2 = WorkoutDay.objects.create(
            program=self.program,
            day_number=2,
            title="Day 2 - Test Workout",
            duration=30,
        )

        # Default login as normal user
        self.client.force_login(self.normal_user)

    def test_user_analytics_no_completions(self):
        """Test analytics with no workout completions"""
        url = reverse('user-analytics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        analytics = response.data['analytics']
        monthly_challenge = response.data['monthlyChallenge']
        
        self.assertEqual(analytics['weeklyImprovement'], 0)
        self.assertEqual(analytics['consistency'], 0)
        self.assertEqual(analytics['xp_last_30_days'], 0)
        self.assertEqual(analytics['current_streak'], 0)
        self.assertIn('target', monthly_challenge)
        self.assertIn('completed', monthly_challenge)


    def test_user_weekly_activity(self):
        """Test weekly activity data"""
        # Create completion for today
        WorkoutDayCompletion.objects.create(
            user_profile=self.normal_profile,
            workout_day=self.workout_day_1,
            completed_at=timezone.now()
        )
        
        url = reverse('weekly-activity')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 7)  # 7 days of week
        self.assertIn('label', response.data[0])
        self.assertIn('date', response.data[0])
        self.assertIn('count', response.data[0])
        self.assertIn('height', response.data[0])
        self.assertIn('isActive', response.data[0])


    # @override_settings(TIME_ZONE='UTC', USE_TZ=True)
    # def test_user_analytics_with_completions(self):
    #     """Test analytics with workout completions"""
    #     # Use timezone-aware datetimes
    #     today_date = timezone.localdate()
    #     yesterday_date = today_date - timedelta(days=1)
        
    #     # Get the current timezone
    #     current_tz = timezone.get_current_timezone()
        
    #     # Create timezone-aware datetime at noon
    #     today_dt = timezone.datetime.combine(
    #         today_date,
    #         timezone.datetime.min.time().replace(hour=12)
    #     ).replace(tzinfo=current_tz)
        
    #     yesterday_dt = timezone.datetime.combine(
    #         yesterday_date,
    #         timezone.datetime.min.time().replace(hour=12)
    #     ).replace(tzinfo=current_tz)

    #     WorkoutDayCompletion.objects.create(
    #         user_profile=self.normal_profile,
    #         workout_day=self.workout_day_1,
    #         xp_earned=30,
    #         completed_at=yesterday_dt
    #     )

    #     WorkoutDayCompletion.objects.create(
    #         user_profile=self.normal_profile,
    #         workout_day=self.workout_day_2,
    #         xp_earned=30,
    #         completed_at=today_dt
    #     )

    #     # Debug: Check what's actually happening
    #     completions = WorkoutDayCompletion.objects.filter(user_profile=self.normal_profile)
        
    #     print("=== DEBUG INFO ===")
    #     print(f"Today datetime: {today_dt}")
    #     print(f"Yesterday datetime: {yesterday_dt}")
        
    #     for comp in completions:
    #         print(f"Completion: {comp.completed_at} -> date: {comp.completed_at.date()}")
        
    #     completion_dates = set(completions.values_list("completed_at__date", flat=True))
    #     print(f"Unique completion dates: {completion_dates}")
    #     print("==================")

    #     url = reverse('user-analytics')
    #     response = self.client.get(url)
        
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     analytics = response.data['analytics']
        
    #     print(f"Calculated streak: {analytics['current_streak']}")
    #     self.assertEqual(analytics['xp_last_30_days'], 60)
    #     self.assertEqual(analytics['current_streak'], 2)
    def test_user_analytics_with_completions(self):
        today = timezone.localdate()
        yesterday = today - timedelta(days=1)
        
        # Create completion (will have current timestamp)
        comp1 = WorkoutDayCompletion.objects.create(
            user_profile=self.normal_profile,
            workout_day=self.workout_day_1,
            xp_earned=30,
        )
        
        # Update timestamp directly in database (bypasses auto_now_add)
        WorkoutDayCompletion.objects.filter(pk=comp1.pk).update(
            completed_at=timezone.datetime.combine(
                yesterday,
                timezone.datetime.min.time().replace(hour=12)
            ).replace(tzinfo=timezone.get_current_timezone())
        )
        
        # Refresh from DB to get new value
        comp1.refresh_from_db()
        self.assertEqual(comp1.completed_at.date(), yesterday)
        # Create second completion
        WorkoutDayCompletion.objects.create(
            user_profile=self.normal_profile,
            workout_day=self.workout_day_2,
            xp_earned=30,
        ) 

        url = reverse('user-analytics')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        analytics = response.data['analytics']
        
        self.assertEqual(analytics['xp_last_30_days'], 60)
        self.assertEqual(analytics['current_streak'], 2)
        
