from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify


class Service(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    service_name = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='services',
    )

    status = models.CharField(
        choices=Status.choices,
        default=Status.DRAFT,
        max_length=2
    )

    class Meta:
        db_table = 'service'
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

        ordering = ['-published']
        indexes = [
            models.Index(fields=['-published'], name='publication_index'),
            models.Index(fields=['price'], name='price_index'),
        ]

    def save(self, **kwargs):
        self.slug = slugify(self.service_name) + '-by-' + slugify(self.provider_name)
        super(Service, self).save()

    def __str__(self):
        return f"{self.service_name} by {self.provider_name}"
