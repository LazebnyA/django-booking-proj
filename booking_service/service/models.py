from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

from taggit.managers import TaggableManager

from comments.models import Comment


class PublishedManager(models.Manager):
    def get_queryset(self):
        return (
            super().get_queryset().filter(status=Service.Status.PUBLISHED)
        )


class Service(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    service_name = models.CharField(max_length=100)
    provider_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique_for_date='published')
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

    objects = models.Manager()
    published_objects = PublishedManager()

    tags = TaggableManager()

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

    def get_absolute_url(self):
        return reverse(
            'service:service_detail',
            args=[self.published.year, self.published.month, self.published.day, self.slug]
        )


class ServiceComment(Comment):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    def __str__(self):
        return (f"Comment by {self.name}. "
                f"Email: {self.email}. "
                f"Service: {self.service.service_name}."
                f"Content: {self.content[:30]}. "
                f"Created: {self.created_date}")

