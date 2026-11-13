from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Feedback(models.Model):
    user_id = models.BigIntegerField('Telegram ID')
    rating = models.PositiveSmallIntegerField('Baho', validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField('Izoh', blank=True, max_length=1000)
    source = models.CharField('Manba', blank=True, max_length=64)
    created_at = models.DateTimeField('Vaqti', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Fikr'
        verbose_name_plural = 'Fikrlar'

    def __str__(self):
        return f'{self.user_id}: {self.rating}'
