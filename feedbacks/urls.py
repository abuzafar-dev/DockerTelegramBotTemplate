from django.urls import path

from feedbacks.views import create_feedback, stats

urlpatterns = [
    path('feedback/', create_feedback, name='feedback-create'),
    path('feedback/stats/', stats, name='feedback-stats'),
]
