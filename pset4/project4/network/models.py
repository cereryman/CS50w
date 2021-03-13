from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField(blank=True, max_length=280)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField("User", related_name="post_likes", blank=True)

    def num_likes(self):
        return self.like.count()


class Like(models.Model):
    liker = models.ForeignKey("User", on_delete=models.CASCADE, related_name="liker")
    liked = models.ForeignKey("Post", default=0, on_delete=models.CASCADE, related_name="liked")

class Follow(models.Model):
    follower = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")