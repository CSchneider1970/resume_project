from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth.models import User
from django.urls import reverse
from jobapp.models import Resume


class ResumeAPITestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="horst", password="password")
        self.user2 = User.objects.create_user(username="karl", password="password")
        self.resume = Resume.objects.create(
            user=self.user1,
            title="Horst Hrubesch",
            bio="Footballer and Coach",
            address="HSV",
        )
        self.token_user1 = AccessToken.for_user(self.user1)
        self.token_user2 = AccessToken.for_user(self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token_user1}")

    def test_owner_can_view_resume(self):
        # self.client.login(username="horst", password="password")
        # response = self.client.get(f"/api/v3/resumes/{self.resume.id}/")
        response = self.client.get(reverse('resume-detail', kwargs={'pk': self.resume.id}))  # Hardcoded URL replaced
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_owner_cannot_update_resume(self):
        # self.client.login(username="karl", password="password")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token_user2}")
        response = self.client.put(
            f"/api/v3/resumes/{self.resume.id}/",
            {"name": "Paul Breitner", "bio": "Updated Bio", "address": "FCB"},
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_resume(self):
        # self.client.login(username="horst", password="password")
        response = self.client.delete(f"/api/v3/resumes/{self.resume.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_owner_cannot_delete_resume(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token_user2}")
        response = self.client.delete(f"/api/v3/resumes/{self.resume.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_create_resume(self):
        # self.client.login(username="karl", password="password")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token_user2}")
        response = self.client.post(
            "/api/v3/resumes/",
            {
                "title": "Karl-Heinz Rummenigge",
                "bio": "Footballer and Executive",
                "address": "Munich",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["user"], self.user2.id)

    def test_authenticated_user_can_reorder_resume(self):
        # self.client.login(username="karl", password="password")
        payload = {"job_history": 1, "skills": 0, "education_history": 2}
        response = self.client.put(
            f"/api/v3/resumes/{self.resume.id}/reorder/", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ["skills", "job_history", "education_history"])
