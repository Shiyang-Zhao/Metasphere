from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import os


class Post(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(null=True, blank=True, upload_to='Files')
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def delete(self, *args, **kwargs):
        # Delete the associated file from the local file system
        if self.file:
            file_path = self.file.path
            # Delete the file from the local file system
            if os.path.exists(file_path):
                os.remove(file_path)

        # Call the base delete() method to remove the post from the database
        super().delete(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['date_posted']

    def __str__(self):
        return self.content[:50]

    def get_absolute_url(self):
        return reverse('comment-reply', kwargs={'comment_pk': self.pk})

    @property
    def children(self):
        return Comment.objects.filter(parent_comment=self).order_by('date_posted')

    @property
    def is_parent(self):
        return self.parent_comment is None
