from django.test import TestCase
from users.models import User, UserProfile
from coach.models import Coach
from coach.serializers import CoachSerializer


class CoachTests(TestCase):
    """Tests for the Coach model and its serializer."""

    def setUp(self):
        """Set up test users and profiles."""
        self.user1 = User.objects.create_user(
            username="coachuser1",
            password="pass123",
            first_name="John",
            last_name="Health",
        )
        self.profile1, _ = UserProfile.objects.get_or_create(user=self.user1)

        self.user2 = User.objects.create_user(
            username="coachuser2",
            password="pass123",
            first_name="Jane",
            last_name="Quest",
        )
        self.profile2, _ = UserProfile.objects.get_or_create(user=self.user2)

    def test_coach_creation_defaults(self):
        """Test default values upon coach creation."""
        coach = Coach.objects.create(user=self.profile1)
        self.assertEqual(coach.status_approval, "pending")
        self.assertIsNone(coach.public_id)
        self.assertIsNone(coach.approved_date)

    def test_public_id_and_approved_date_generated_on_approval(self):
        """Test that public_id and approved_date are set when status is approved."""
        coach = Coach.objects.create(user=self.profile1)
        coach.status_approval = "approved"
        coach.save()
        coach.refresh_from_db()

        self.assertTrue(coach.public_id.startswith("C-"))
        self.assertEqual(len(coach.public_id), 7)
        self.assertIsNotNone(coach.approved_date)

    def test_public_id_not_regenerated_if_exists(self):
        """Test that public_id and approved_date are not changed on subsequent saves."""
        coach = Coach.objects.create(user=self.profile1)
        coach.status_approval = "approved"
        coach.save()
        first_id = coach.public_id
        first_date = coach.approved_date

        coach.save()
        coach.refresh_from_db()

        self.assertEqual(coach.public_id, first_id)
        self.assertEqual(coach.approved_date, first_date)

    def test_str_representation(self):
        """Test the string representation of the Coach model."""
        coach = Coach.objects.create(user=self.profile1)
        expected = f"Coach: {self.user1.username} (No ID) - Status: pending"
        self.assertEqual(str(coach), expected)

        coach.status_approval = "approved"
        coach.save()
        coach.refresh_from_db()
        self.assertIn("Coach: coachuser1 (C-", str(coach))
        self.assertIn("Status: approved", str(coach))

    def test_serializer_name_field(self):
        """Test that the serializer returns the correct name field."""
        coach = Coach.objects.create(user=self.profile2)
        serializer = CoachSerializer(coach)
        self.assertEqual(serializer.data["name"], "Jane Quest")

    def test_serializer_fallback_to_username(self):
        """Test that the serializer falls back 
        to username if name fields are missing."""
        self.user2.first_name = ""
        self.user2.last_name = ""
        self.user2.save()
        coach = Coach.objects.create(user=self.profile2)
        serializer = CoachSerializer(coach)
        self.assertEqual(serializer.data["name"], self.user2.username)

    def test_serializer_no_certification_doc(self):
        """Test that the serializer handles missing certification document."""
        coach = Coach.objects.create(user=self.profile2)
        serializer = CoachSerializer(coach)
        self.assertIsNone(serializer.data["certification_doc"])

    def test_status_invalid_value(self):
        """Test that setting an invalid status does not break the model."""
        coach = Coach.objects.create(user=self.profile1)
        coach.status_approval = "unknown"
        coach.save()
        self.assertEqual(coach.status_approval, "unknown")

    def test_approve_generates_unique_public_id(self):
        """Test that multiple approved coaches get unique public IDs."""
        coach1 = Coach.objects.create(user=self.profile1)
        coach1.status_approval = "approved"
        coach1.save()

        coach2 = Coach.objects.create(user=self.profile2)
        coach2.status_approval = "approved"
        coach2.save()

        self.assertNotEqual(coach1.public_id, coach2.public_id)

    def test_string_representation_for_rejected_status(self):
        """Test string representation for a rejected coach."""
        coach = Coach.objects.create(user=self.profile1)
        coach.status_approval = "rejected"
        coach.save()
        self.assertIn("rejected", str(coach))
