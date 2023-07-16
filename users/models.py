from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(
        default='default_profile.jpg', upload_to='profile_pics')
    following = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name='followers')
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        img.save(self.image.path)

    def update_activity(self):
        self.last_activity = timezone.now()
        self.save()

    @property
    def is_online(self):
        return self.last_activity >= timezone.now() - timedelta(minutes=5)
