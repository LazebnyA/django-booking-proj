from django.db import models


class Feedback(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:25]

    class Meta:
        db_table = 'feedback'
        ordering = ['created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'
