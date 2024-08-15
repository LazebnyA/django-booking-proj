from django.db import models


class Comment(models.Model):
    name = models.CharField(max_length=25)
    email = models.EmailField()
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        db_table = 'comments'
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

        ordering = ['created_date']
        indexes = [
            models.Index(fields=['created_date']),
        ]

    def __str__(self):
        return (f"Comment by {self.name}. "
                f"Email: {self.email}. "
                f"Content: {self.content[:30]}. "
                f"Created: {self.created_date}")
