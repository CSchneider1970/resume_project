from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import (
    BasicAuthentication,
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .models import Resume
from .serializers import (
    ResumeSerializer,
    JobHistorySerializer,
    SkillSerializer,
    EducationHistorySerializer,
)
from .permissions import IsOwnerOrReadOnly


class ResumeList(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [
        BasicAuthentication,
        SessionAuthentication,
        TokenAuthentication,
        JWTAuthentication,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ResumeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer
    permission_classes = (IsOwnerOrReadOnly,)


# class ResumeReorderView(APIView):
#     permission_classes = (permissions.IsAuthenticated,)

#     def put(self, request, pk):
#         resume = get_object_or_404(Resume, pk=pk)
#         data = request.data

#         expected_keys = {"job_history", "skills", "education_history"}
#         received_keys = set(data.keys())  # Remove duplicates

#         # All three keys must be present
#         if expected_keys != received_keys:
#             return Response(
#                 {
#                     "error": "Payload must contain job_history, skills, and education_history."
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Checking the values for uniqueness
#         values = list(data.values())
#         if len(values) != len(set(values)):
#             return Response(
#                 {"error": "Order values must be unique."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         # Concatinate all sections
#         resume_sections = {
#             "job_history": JobHistorySerializer(resume.job_history.all(), many=True).data,
#             "skills": SkillSerializer(resume.skills.all(), many=True).data,
#             "education_history": EducationHistorySerializer(resume.education_history.all(), many=True).data,
#         }

#         # Sort the resume sections based on the put request data
#         ordered_sections = sorted(resume_sections.items(), key=lambda item: data[item[0]])

#         # Create the reponse as a dictionary from the tuple list
#         response_data = {key: value for key, value in ordered_sections}

#         return Response(response_data, status=status.HTTP_200_OK)


class ResumeReorderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, pk):
        resume = get_object_or_404(Resume, pk=pk)
        data = request.data

        expected_keys = {"job_history", "skills", "education_history"}
        received_keys = set(data.keys())

        # All three keys must be present
        if expected_keys != received_keys:
            return Response(
                {"error": "Payload must contain job_history, skills, and education_history."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Checking the values for uniqueness
        values = list(data.values())
        if len(values) != len(set(values)):
            return Response(
                {"error": "Order values must be unique."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Save the new order in the Resume model
        resume.job_history_order = data["job_history"]
        resume.skills_order = data["skills"]
        resume.education_history_order = data["education_history"]
        resume.save()

        # Concatinate all sections
        resume_sections = {
            "job_history": JobHistorySerializer(resume.job_history.all(), many=True).data,
            "skills": SkillSerializer(resume.skills.all(), many=True).data,
            "education_history": EducationHistorySerializer(resume.education_history.all(), many=True).data,
        }

        # Sort the resume sections based on the put request data
        ordered_sections = sorted(resume_sections.items(), key=lambda item: data[item[0]])

        # Create the reponse as a dictionary from the tuple list
        response_data = {key: value for key, value in ordered_sections}

        return Response(response_data, status=status.HTTP_200_OK)


