from django.contrib import admin

from feedbacks.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'rating', 'source', 'created_at']
    list_filter = ['rating', 'source']
    search_fields = ['comment', 'source']
