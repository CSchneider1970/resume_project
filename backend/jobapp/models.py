from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, help_text="A simple Help-Text")
    name = models.CharField(max_length=255)
    bio = models.TextField()
    address = models.CharField(max_length=255)

    def __str__(self):
        if self.user:
            return self.user.username
        return f"Resume {self.id} (no user)"


class JobHistory(models.Model):
    resume = models.ForeignKey(Resume, related_name='job_history', on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)  # null if currently employed
    order = models.PositiveIntegerField(null=True)


class Skill(models.Model):
    resume = models.ForeignKey(Resume, related_name='skills', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    order = models.PositiveIntegerField(null=True)


class EducationHistory(models.Model):
    resume = models.ForeignKey(Resume, related_name='education_history', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    order = models.PositiveIntegerField(null=True)
