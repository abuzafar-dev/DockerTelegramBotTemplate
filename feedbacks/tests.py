import json

from django.test import TestCase, override_settings

from feedbacks.models import Feedback


@override_settings(API_TOKEN='test-token')
class FeedbackApiTests(TestCase):
    url = '/api/feedback/'

    def post(self, data, token='test-token'):
        return self.client.post(self.url, json.dumps(data), content_type='application/json', HTTP_X_API_TOKEN=token)

    def test_create(self):
        response = self.post({'user_id': 123, 'rating': 4, 'comment': 'Zo\'r', 'source': 'filial_3'})
        self.assertEqual(response.status_code, 201)
        feedback = Feedback.objects.get()
        self.assertEqual((feedback.user_id, feedback.rating, feedback.source), (123, 4, 'filial_3'))

    def test_rating_out_of_range(self):
        response = self.post({'user_id': 123, 'rating': 9})
        self.assertEqual(response.status_code, 400)
        self.assertIn('rating', response.json()['errors'])
        self.assertFalse(Feedback.objects.exists())

    def test_wrong_token(self):
        response = self.post({'user_id': 123, 'rating': 5}, token='xato')
        self.assertEqual(response.status_code, 403)

    def test_bad_json_and_method(self):
        response = self.client.post(self.url, 'salom', content_type='application/json', HTTP_X_API_TOKEN='test-token')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.get(self.url).status_code, 405)

    def test_stats(self):
        Feedback.objects.create(user_id=1, rating=5)
        Feedback.objects.create(user_id=2, rating=2)
        self.assertEqual(self.client.get('/api/feedback/stats/').json(), {'count': 2, 'average': 3.5})
