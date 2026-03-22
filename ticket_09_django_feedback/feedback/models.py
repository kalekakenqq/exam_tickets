from django.db import models


class Feedback(models.Model):
    name = models.CharField(max_length=100, verbose_name='имя')
    email = models.EmailField(verbose_name='email')
    message = models.TextField(verbose_name='сообщение')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.email})'

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-created_at']
