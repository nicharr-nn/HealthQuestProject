# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from rest_framework.test import APIClient

# from coach.models import Coach
# from workout import models as workout_models

# User = get_user_model()


# class WorkoutProgramAccessTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_normal_user_sees_only_public_programs(self):
#         """
#         Normal user should only see public programs, not private ones.
#         """
#         pass

#         member = User.objects.create_user(username="member1", password="pass")

#         coach_user1 = User.objects.create_user(
#             username="coach1", password="pass"
#         )
#         coach1 = Coach.objects.create(
#             user=coach_user1.userprofile, status_approval="approved"
#         )

#         coach_user2 = User.objects.create_user(
#             username="coach2", password="pass"
#         )
#         coach2 = Coach.objects.create(
#             user=coach_user2.userprofile, status_approval="approved"
#         )

#         WP = workout_models.WorkoutProgram

#         WP.objects.create(
#             title="Public Program",
#             description="Public",
#             difficulty_level="easy",
#             duration=1,
#             category="general",
#             is_public=True,
#             # pass the UserProfile (coach1.user) not the Coach instance
#             **(
#                 {"coach": coach1.user}
#                 if "coach" in [f.name for f in WP._meta.get_fields()]
#                 else {}
#             ),
#         )

#         WP.objects.create(
#             title="Private Program",
#             description="Private",
#             difficulty_level="easy",
#             duration=1,
#             category="general",
#             is_public=False,
#             **(
#                 {"coach": coach2.user}
#                 if "coach" in [f.name for f in WP._meta.get_fields()]
#                 else {}
#             ),
#         )

#         self.client.force_authenticate(user=member)
#         resp = self.client.get("/api/workout/programs/")
#         self.assertEqual(resp.status_code, 200)

#         data = (
#             resp.data["results"]
#             if isinstance(resp.data, dict) and "results" in resp.data
#             else resp.data
#         )
#         titles = {p.get("title") for p in data}
#         self.assertIn("Public Program", titles)
#         self.assertNotIn("Private Program", titles)

#     def test_coach_sees_private_programs_for_their_own_account(self):
#         """
#         A coach should be able to see their own private programs.
#         """
#         coach_user = User.objects.create_user(
#             username="coachx", password="pass"
#         )
#         # mark profile as coach so view's role check passes
#         coach_user.userprofile.role = "coach"
#         coach_user.userprofile.save()
#         coach = Coach.objects.create(
#             user=coach_user.userprofile, status_approval="approved"
#         )

#         WP = workout_models.WorkoutProgram
#         WP.objects.create(
#             title="CoachPrivate",
#             description="Private",
#             difficulty_level="easy",
#             duration=1,
#             category="general",
#             is_public=False,
#             **(
#                 {"coach": coach.user}
#                 if "coach" in [f.name for f in WP._meta.get_fields()]
#                 else {}
#             ),
#         )

#         self.client.force_authenticate(user=coach_user)
#         resp = self.client.get("/api/workout/programs/")
#         self.assertEqual(resp.status_code, 200)

#         data = (
#             resp.data["results"]
#             if isinstance(resp.data, dict) and "results" in resp.data
#             else resp.data
#         )
#         titles = {p.get("title") for p in data}
#         self.assertIn("CoachPrivate", titles)


# # Run tests with pytest in backend
# # python manage.py test coach
