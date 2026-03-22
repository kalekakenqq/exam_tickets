from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(blank=True, verbose_name='описание')
    completed = models.BooleanField(default=False, verbose_name='выполнено')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'задача'
        verbose_name_plural = 'задачи'
