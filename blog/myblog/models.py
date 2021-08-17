from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Post(models.Model):
    """ Модель поста """

    h1 = models.CharField(max_length=200, verbose_name='Heading')
    title = models.CharField(max_length=200, verbose_name='Title')
    url = models.SlugField(verbose_name='url')
    description = RichTextUploadingField(verbose_name='Description')
    content = RichTextUploadingField(verbose_name='Content')
    image = models.ImageField(verbose_name='Image')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data create')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    tag = TaggableManager(verbose_name='Tag')

    def __str__(self):
        return f'{self.title} - {self.author}'
