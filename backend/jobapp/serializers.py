from rest_framework import serializers
from .models import EducationHistory, JobHistory, Resume, Skill

class EducationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationHistory
        fields = ('name', 'qualification')


class JobHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHistory
        fields = ('job_title', 'description', 'start_date', 'end_date')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name', 'rating')


class ResumeSerializer(serializers.ModelSerializer):
    education_history = EducationHistorySerializer(many=True, required=False)
    skills = SkillSerializer(many=True,required=False)
    job_history = JobHistorySerializer(many=True, required=False)

    class Meta:
        model = Resume
        fields = ('id', 'user', 'name', 'bio', 'skills', 'address', 'job_history', 'education_history')
