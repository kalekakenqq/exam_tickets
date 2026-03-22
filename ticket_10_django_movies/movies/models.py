from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    director = models.CharField(max_length=100, verbose_name='режиссёр')
    year = models.IntegerField(verbose_name='год')
    rating = models.FloatField(verbose_name='рейтинг')
    description = models.TextField(blank=True, verbose_name='описание')

    def __str__(self):
        return f'{self.title} ({self.year})'

    class Meta:
        verbose_name = 'фильм'
        verbose_name_plural = 'фильмы'
        ordering = ['-rating']
