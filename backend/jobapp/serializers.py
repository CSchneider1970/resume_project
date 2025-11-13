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

    def create(self, validated_data):
        education_history_data = validated_data.pop('education_history', [])
        skills_data = validated_data.pop('skills', [])
        job_history_data = validated_data.pop('job_history', [])

        resume = Resume.objects.create(**validated_data)

        for job in job_history_data:
            JobHistory.objects.create(resume=resume, **job)
        for skill in skills_data:
            Skill.objects.create(resume=resume, **skill)
        for education in education_history_data:
            EducationHistory.objects.create(resume=resume, **education)

        return resume

    def update(self, instance, validated_data):
        education_history_data = validated_data.pop('education_history', [])
        skills_data = validated_data.pop('skills', [])
        job_history_data = validated_data.pop('job_history', [])

        # Update simple fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        '''
        For testing disabled to avoid data loss

        # Clear old related objects
        instance.job_history.all().delete()
        instance.skills.all().delete()
        instance.education_history.all().delete()

        # Recreate related objects
        for job in job_history_data:
            JobHistory.objects.create(resume=instance, **job)
        for skill in skills_data:
            Skill.objects.create(resume=instance, **skill)
        for education in education_history_data:
            EducationHistory.objects.create(resume=instance, **education)
        '''

        # Delete only and recreate if data is provided
        if job_history_data is not None:
            instance.job_history.all().delete()
            for job in job_history_data:
                JobHistory.objects.create(resume=instance, **job)

        if skills_data is not None:
            instance.skills.all().delete()
            for skill in skills_data:
                Skill.objects.create(resume=instance, **skill)

        if education_history_data is not None:
            instance.education_history.all().delete()
            for education in education_history_data:
                EducationHistory.objects.create(resume=instance, **education)

        return instance
