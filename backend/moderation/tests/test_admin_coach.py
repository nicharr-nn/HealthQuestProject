from django.urls import reverse
from rest_framework import status
from .test_admin import AdminTestBase


class AdminCoachTests(AdminTestBase):
    """Tests for admin actions on coach approvals."""

    def test_admin_can_approve_coach(self):
        """Test that an admin can approve a pending coach."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("approve_coach", kwargs={"coach_id": self.coach.pk})
        response = self.client.post(url, {"reason": "Valid credentials"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.coach.refresh_from_db()
        self.assertEqual(self.coach.status_approval, "approved")

    def test_admin_can_reject_coach(self):
        """Test that an admin can reject a pending coach."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("reject_coach", kwargs={"coach_id": self.coach.pk})
        response = self.client.post(url, {"reason": "Invalid credentials"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.coach.refresh_from_db()
        self.assertEqual(self.coach.status_approval, "rejected")

    def test_non_admin_cannot_approve_coach(self):
        """Test that non-admin users cannot approve a coach."""
        self.client.force_authenticate(user=self.member_user)
        url = reverse("approve_coach", kwargs={"coach_id": self.coach.pk})
        response = self.client.post(url, {"reason": "Try to approve"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_approve_nonexistent_coach(self):
        """Test approving a nonexistent coach returns 404."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("approve_coach", kwargs={"coach_id": 9999})
        response = self.client.post(url, {"reason": "Test"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_reject_nonexistent_coach(self):
        """Test rejecting a nonexistent coach returns 404."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("reject_coach", kwargs={"coach_id": 9999})
        response = self.client.post(url, {"reason": "Test"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_approve_already_approved_coach(self):
        """Test approving an already approved coach returns appropriate response."""
        self.coach.status_approval = "approved"
        self.coach.save()
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("approve_coach", kwargs={"coach_id": self.coach.pk})
        response = self.client.post(url, {"reason": "Already approved"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.coach.refresh_from_db()
        self.assertEqual(self.coach.status_approval, "approved")

    def test_non_admin_cannot_reject_coach(self):
        """Test that non-admin users cannot reject a coach."""
        self.client.force_authenticate(user=self.coach_user)
        url = reverse("reject_coach", kwargs={"coach_id": self.coach.pk})
        response = self.client.post(url, {"reason": "Try reject"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
