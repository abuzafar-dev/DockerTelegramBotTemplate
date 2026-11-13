import json
import secrets

from django.conf import settings
from django.db.models import Avg, Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from feedbacks.forms import FeedbackForm
from feedbacks.models import Feedback


def token_ok(request):
    if not settings.API_TOKEN:
        return True
    return secrets.compare_digest(request.headers.get('X-Api-Token', ''), settings.API_TOKEN)


@csrf_exempt
@require_POST
def create_feedback(request):
    if not token_ok(request):
        return JsonResponse({'error': "Token noto'g'ri"}, status=403)
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'error': "JSON noto'g'ri"}, status=400)
    if not isinstance(data, dict):
        return JsonResponse({'error': "JSON noto'g'ri"}, status=400)
    form = FeedbackForm(data)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors}, status=400)
    feedback = form.save()
    return JsonResponse({'id': feedback.id}, status=201)


@require_GET
def stats(request):
    result = Feedback.objects.aggregate(count=Count('id'), average=Avg('rating'))
    result['average'] = round(result['average'] or 0, 2)
    return JsonResponse(result)
