from rest_framework import serializers
from .models import EducationHistory, JobHistory, Resume, Skill

class EducationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationHistory
        fields = ('institution', 'degree', 'start_date', 'end_date')


class JobHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobHistory
        fields = ('job_title', 'company', 'description', 'start_date', 'end_date')


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('name', 'skill_level')


class ResumeSerializer(serializers.ModelSerializer):
    education_history = EducationHistorySerializer(many=True, required=False)
    skills = SkillSerializer(many=True,required=False)
    job_history = JobHistorySerializer(many=True, required=False)

    class Meta:
        model = Resume
        fields = (
            'id', 'user', 'title', 'bio', 'address',
            'job_history_order', 'skills_order', 'education_history_order',
            'skills', 'job_history', 'education_history'
        )

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

    def to_representation(self, instance):
        # Get the default representation
        data = super().to_representation(instance)

        # Collect sections with their order
        sections = [
            ("job_history", data["job_history"], instance.job_history_order),
            ("skills", data["skills"], instance.skills_order),
            ("education_history", data["education_history"], instance.education_history_order),
        ]

        # Sort sections based on the stored order
        ordered_sections = sorted(sections, key=lambda x: x[2])

        # Create a new ordered representation
        ordered_data = {
            "id": data["id"],
            "user": data["user"],
            "title": data["title"],
            "bio": data["bio"],
            "address": data["address"],
        }

        for key, value, _ in ordered_sections:
            ordered_data[key] = value

        return ordered_data
    