# from django.contrib.auth import get_user_model
# from django.urls import reverse
# from rest_framework.test import APIClient, APITestCase

# # try to import models from the workout app, fallback to users app if needed
# try:
#     from workout.models import WorkoutAssignment, WorkoutProgram
# except Exception:
#     try:
#         from users.models import WorkoutAssignment, WorkoutProgram  # fallback
#     except Exception:
#         WorkoutProgram = None
#         WorkoutAssignment = None

# # helper: try to import UserProfile / UserLevel if present
# try:
#     from users.models import UserLevel, UserProfile
# except Exception:
#     UserProfile = None
#     UserLevel = None

# User = get_user_model()


# class WorkoutDayCompletionTest(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = User.objects.create_user(
#             username="testuser", password="testpass"
#         )
#         # ensure profile exists if there is a UserProfile model
#         if UserProfile:
#             self.profile = getattr(
#                 self.user, "userprofile", None
#             ) or UserProfile.objects.create(user=self.user)
#             # make this user a member so they can complete assignments in tests
#             self.profile.role = "member"
#             self.profile.save()
#         else:
#             self.profile = getattr(self.user, "userprofile", None)

#         # create a minimal program (use field names that exist)
#         prog_kwargs = {}
#         if WorkoutProgram is None:
#             self.skipTest("WorkoutProgram model not available")
#         else:
#             fields = [f.name for f in WorkoutProgram._meta.get_fields()]
#             if "title" in fields:
#                 prog_kwargs["title"] = "Test Program"

#             # ensure we set the required coach/owner field if present (use the test user's profile)
#             if "coach" in fields:
#                 prog_kwargs["coach"] = self.profile
#             elif "owner" in fields:
#                 prog_kwargs["owner"] = self.profile
#             elif "created_by" in fields:
#                 prog_kwargs["created_by"] = self.profile

#             # create with any defaults for other fields
#             self.program = WorkoutProgram.objects.create(**prog_kwargs)

#         # create assignment: try user then profile
#         if WorkoutAssignment is None:
#             self.skipTest("WorkoutAssignment model not available")
#         else:
#             try:
#                 self.assignment = WorkoutAssignment.objects.create(
#                     user=self.user, program=self.program
#                 )
#             except Exception:
#                 # fallback to user_profile or profile field
#                 try:
#                     self.assignment = WorkoutAssignment.objects.create(
#                         user_profile=self.profile, program=self.program
#                     )
#                 except Exception:
#                     # last resort: create without linking fields (test will likely fail)
#                     self.assignment = WorkoutAssignment.objects.create(
#                         program=self.program
#                     )

#         self.client.force_authenticate(user=self.user)

#     def _get_xp(self):
#         # return integer xp for assertions or None if not found
#         if self.profile and hasattr(self.profile, "xp"):
#             return getattr(self.profile, "xp") or 0
#         if UserLevel:
#             lvl = UserLevel.objects.filter(user_profile=self.profile).first()
#             if lvl:
#                 return getattr(lvl, "xp", 0) or 0
#         return None

#     def test_complete_workout_awards_xp(self):
#         pass
#         # call the member "complete assignment" endpoint (PATCH)
#         url = reverse(
#             "workout-assignment-update", kwargs={"id": self.assignment.id}
#         )
#         resp = self.client.patch(url, {}, format="json")
#         self.assertEqual(resp.status_code, 200)

#         # verify XP was awarded
#         xp_awarded = resp.data.get("xp_awarded", 0)
#         self.assertGreater(xp_awarded, 0, "Expected XP to be awarded")

#         # verify assignment completed — prefer status field, fall back to boolean/date flags
#         status_val = getattr(self.assignment, "status", None)

#         def _check_boolean_flags(obj):
#             completed = getattr(obj, "completed", None)
#             if completed is None:
#                 completed = getattr(obj, "is_completed", None)
#             if not completed:
#                 completed = bool(
#                     getattr(obj, "completed_at", None)
#                     or getattr(obj, "completed_date", None)
#                 )
#             return bool(completed)

#         if status_val is not None:
#             # accept explicit completed-like status values OR rely on boolean/timestamp flags
#             if status_val in ("completed", "done", "finished"):
#                 pass
#             else:
#                 self.assertTrue(
#                     _check_boolean_flags(self.assignment),
#                     msg=f"Assignment was not marked completed (status={status_val})",
#                 )

#         else:
#             self.assertTrue(
#                 _check_boolean_flags(self.assignment),
#                 "Assignment was not marked completed",
#             )


# # Run tests with pytest in backend
# # python manage.py test workout
