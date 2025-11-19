from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from users.models import UserProfile, UserLevel
from workout.models import WorkoutProgram

User = get_user_model()


class WorkoutProgramFilteringTests(TestCase):
    """Test workout program filtering by role"""

    def setUp(self):
        self.client = APIClient()

        # Create Coach 1
        self.coach1 = User.objects.create_user(
            username="coach1", email="coach1@test.com", password="test123"
        )
        self.coach1_profile = self.coach1.userprofile
        self.coach1_profile.role = "coach"
        self.coach1_profile.save()
        self.coach1_profile.refresh_from_db()
        
        # Ensure level exists
        # UserLevel.objects.get_or_create(
        #     user_profile=self.coach1_profile,
        #     defaults={
        #         'level': 'Bronze',
        #         'level_rank': 1,
        #         'xp': 0,
        #         'goal_achieved': False,
        #     }
        # )

        # Create Coach 2
        self.coach2 = User.objects.create_user(
            username="coach2", email="coach2@test.com", password="test123"
        )
        self.coach2_profile = self.coach2.userprofile
        self.coach2_profile.role = "coach"
        self.coach2_profile.save()
        self.coach2_profile.refresh_from_db()
        
        # # Ensure level exists
        # UserLevel.objects.get_or_create(
        #     user_profile=self.coach2_profile,
        #     defaults={
        #         'level': 'Bronze',
        #         'level_rank': 1,
        #         'xp': 0,
        #         'goal_achieved': False,
        #     }
        # )

        # Coach 1's programs
        self.coach1_program1 = WorkoutProgram.objects.create(
            coach=self.coach1_profile,
            title="Coach 1 Private Program",
            is_public=False,
            level_access="all",
        )
        self.coach1_program2 = WorkoutProgram.objects.create(
            coach=self.coach1_profile,
            title="Coach 1 Public Program",
            is_public=True,
            level_access="all",
        )

        self.coach1_program1.save()
        self.coach1_program2.save()

        # Coach 2's programs
        self.coach2_program1 = WorkoutProgram.objects.create(
            coach=self.coach2_profile,
            title="Coach 2 Private Program",
            is_public=False,
            level_access="all",
        )
        self.coach2_program2 = WorkoutProgram.objects.create(
            coach=self.coach2_profile,
            title="Coach 2 Public Program",
            is_public=True,
            level_access="all",
        )

        self.coach2_program1.save()
        self.coach2_program2.save()

    def test_coach_sees_only_own_programs(self):
        """Coach should only see their own programs, not other coaches' programs"""
        self.client.force_login(self.coach1)

        # Verify the user's role
        self.assertEqual(self.coach1_profile.role, "coach")
        
        url = reverse("workout-programs")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should only see 2 programs (both coach1's)
        self.assertEqual(len(response.data), 2, 
                        f"Expected 2 programs, got {len(response.data)}: {[p['title'] for p in response.data]}")

        # Check by title instead of ID (more reliable)
        program_titles = [p["title"] for p in response.data]
        self.assertIn("Coach 1 Private Program", program_titles)
        self.assertIn("Coach 1 Public Program", program_titles)

        # Should NOT see coach2's programs
        self.assertNotIn("Coach 2 Private Program", program_titles)
        self.assertNotIn("Coach 2 Public Program", program_titles)

        # Also verify by coach relationship
        for program in response.data:
            self.assertEqual(program["coach"], self.coach1_profile.id,
                           f"Program {program['title']} belongs to coach {program['coach']}, expected {self.coach1_profile.id}")

    def test_coach2_sees_only_own_programs(self):
        """Coach 2 should only see their own programs"""
        self.client.force_login(self.coach2)
        
        # Verify the user's role
        self.assertEqual(self.coach2.userprofile.role, "coach")
        
        url = reverse("workout-programs")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Debug output
        if len(response.data) != 2:
            print(f"\n❌ Coach2: Expected 2 programs, got {len(response.data)}")
            print(f"Programs: {[p['title'] for p in response.data]}")
        
        self.assertEqual(len(response.data), 2,
                        f"Expected 2 programs, got {len(response.data)}: {[p['title'] for p in response.data]}")

        # Check by title
        program_titles = [p["title"] for p in response.data]
        self.assertIn("Coach 2 Private Program", program_titles)
        self.assertIn("Coach 2 Public Program", program_titles)

        # Should NOT see coach1's programs
        self.assertNotIn("Coach 1 Private Program", program_titles)
        self.assertNotIn("Coach 1 Public Program", program_titles)

        # Verify by coach relationship
        for program in response.data:
            self.assertEqual(program["coach"], self.coach2_profile.id)

    def test_both_coaches_programs_separate(self):
        """Test that both coaches have separate program sets"""
        # Get coach1's programs
        self.client.force_login(self.coach1)
        response1 = self.client.get(reverse("workout-programs"))
        coach1_titles = {p["title"] for p in response1.data}

        # Get coach2's programs
        self.client.force_login(self.coach2)
        response2 = self.client.get(reverse("workout-programs"))
        coach2_titles = {p["title"] for p in response2.data}

        # Debug
        if coach1_titles & coach2_titles:
            print(f"\n❌ Found overlap: {coach1_titles & coach2_titles}")
            print(f"Coach1 sees: {coach1_titles}")
            print(f"Coach2 sees: {coach2_titles}")

        # No overlap
        self.assertEqual(len(coach1_titles & coach2_titles), 0,
                        f"Programs should not overlap. Coach1: {coach1_titles}, Coach2: {coach2_titles}")

        # Each coach has 2 programs
        self.assertEqual(len(coach1_titles), 2)
        self.assertEqual(len(coach2_titles), 2)

    def test_public_programs_not_visible_to_coaches_in_main_view(self):
        """Coaches should not see other coaches' public programs in main view"""
        self.client.force_login(self.coach1)
        url = reverse("workout-programs")
        response = self.client.get(url)

        # Debug
        if len(response.data) != 2:
            print(f"\n❌ Expected coach1 to see 2 programs, got {len(response.data)}")
            for prog in response.data:
                print(f"  - {prog['title']} (coach_id: {prog['coach']})")

        # Coach1 should only see their own programs
        self.assertEqual(len(response.data), 2,
                        f"Coach should see exactly 2 programs, got {len(response.data)}")

        # Verify none of the programs belong to coach2
        for program in response.data:
            self.assertNotEqual(program["coach"], self.coach2_profile.id,
                              f"Coach1 should not see Coach2's program: {program['title']}")
            self.assertEqual(program["coach"], self.coach1_profile.id,
                           f"All programs should belong to Coach1, but {program['title']} belongs to {program['coach']}")