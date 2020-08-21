from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from django.utils import timezone

# Create your models here.
class TweetManager(models.Manager):
	def retweet(self, user, parent_obj):
		if parent_obj.parent:
			og_parent = parent_obj.parent
		else:
			og_parent = parent_obj
		qs = self.get_queryset().filter(
				tweetUser=user,
				parent=og_parent,
				).filter(
					timestamp__year=timezone.now().year,
					timestamp__month=timezone.now().month,
					timestamp__day=timezone.now().day,
				)
		if qs.exists():
			return None
		obj = self.model(
			parent = og_parent,
			tweetUser = user,
			content = parent_obj.content,
		)
		obj.save()
		return obj

	def liked_toggle(self, user, tweet_obj):
		if user in tweet_obj.liked.all():
			liked_value = False
			tweet_obj.liked.remove(user)
		else:
			liked_value = True
			tweet_obj.liked.add(user)
		return liked_value


class Tweets(models.Model):
	parent = models.ForeignKey("self", null=True, blank=True, on_delete= models.SET_NULL)
	tweetUser = models.ForeignKey(Profile, on_delete= models.SET_NULL, null=True)
	liked = models.ManyToManyField(User, blank=True, related_name='liked')
	content = models.CharField(max_length=140)
	updated = models.DateTimeField(auto_now=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	objects = TweetManager()

	def __str__(self):
		return str(self.content)

	class Meta:
		verbose_name = "Tweet"
		verbose_name_plural = "Tweets"
