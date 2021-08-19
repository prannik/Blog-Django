import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

def get_uploud_path(instance, filename):
    filename = instance.url + '.' + filename.split('.')[1]
    return os.path.join('', filename)

class Post(models.Model):
    """ Модель поста """

    h1 = models.CharField(max_length=200, verbose_name='Heading')
    title = models.CharField(max_length=200, verbose_name='Title')
    url = models.SlugField(verbose_name='url')
    description = RichTextUploadingField(verbose_name='Description')
    content = RichTextUploadingField(verbose_name='Content')
    image = models.ImageField(upload_to=get_uploud_path, blank=True, verbose_name='Image')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Data create')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    tag = TaggableManager(verbose_name='Tag')
    post_likes = models.PositiveIntegerField(default=0, null=True)
    post_dislikes = models.PositiveIntegerField(default=0, null=True)

    def __str__(self):
        return f'{self.title} - {self.author}'

class Comment(models.Model):
    """ Модель Комментариев """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_name')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now, null=True)
    comment_likes = models.PositiveIntegerField(default=0, null=True)
    comment_dislikes = models.PositiveIntegerField(default=0, null=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'Коммент к {self.post.url} от {self.username}'
