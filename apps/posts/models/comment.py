from django.db import models
from django.conf import settings
from .post import Post
from django.urls import reverse


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posted_comments",
    )
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_comments", blank=True
    )
    disliked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="disliked_comments", blank=True
    )
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    attachments = models.FileField(
        upload_to="comment_attachments/", null=True, blank=True
    )
    visibility = models.BooleanField(default=True)
    report_count = models.IntegerField(default=0)

    @property
    def is_parent(self):
        return self.parent_comment is None

    @property
    def children(self):
        return Comment.objects.filter(parent_comment=self)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.date_posted.strftime("%Y-%m-%d %H:%M")}'

    def get_absolute_url(self):
        return reverse("comment-detail", kwargs={"pk": self.pk})

    def like(self, user_pk):
        if not self.liked_by.filter(pk=user_pk).exists():
            self.liked_by.add(user_pk)
            self.disliked_by.remove(user_pk)

    def dislike(self, user_pk):
        if not self.disliked_by.filter(pk=user_pk).exists():
            self.disliked_by.add(user_pk)
            self.liked_by.remove(user_pk)

    # def is_liked_by(self, user):
    #     return self.liked_by.filter(pk=user.pk).exists()

    # def is_disliked_by(self, user):
    #     return self.disliked_by.filter(pk=user.pk).exists()
