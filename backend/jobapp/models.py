from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text="A simple Help-Text")
    title = models.CharField(max_length=255)
    bio = models.TextField()
    address = models.CharField(max_length=255)
    job_history_order = models.PositiveIntegerField(default=0)
    skills_order = models.PositiveIntegerField(default=1)
    education_history_order = models.PositiveIntegerField(default=2)

    def __str__(self):
        if self.user:
            return self.user.username
        return f"Resume {self.id} (no user)"


class JobHistory(models.Model):
    resume = models.ForeignKey(Resume, related_name='job_history', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # null if currently employed
    # order = models.PositiveIntegerField(null=True)


class Skill(models.Model):
    resume = models.ForeignKey(Resume, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    skill_level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    # order = models.PositiveIntegerField(null=True)


class EducationHistory(models.Model):
    resume = models.ForeignKey(Resume, related_name='education_history', on_delete=models.CASCADE)
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # null if currently employed
    # order = models.PositiveIntegerField(null=True)
