from django.db import models
from tweets.models import Tweets

# Create your models here.
class hashtag(models.Model):
    tag = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_tag_tweet(self):
        return Tweets.objects.filter(content__icontains="#" + self.tag).order_by("-timestamp")
