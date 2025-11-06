from django.urls import path
from .views import ResumeList, ResumeDetail, ResumeReorderView

urlpatterns = [
    path('resumes/<int:pk>/', ResumeDetail.as_view(), name='resume-detail'),
    path('resumes/', ResumeList.as_view()),
    path('resumes/<int:pk>/reorder/', ResumeReorderView.as_view(), name='resume-reorder'),
]
