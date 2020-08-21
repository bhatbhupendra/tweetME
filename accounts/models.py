from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.
class UserProfileManager(models.Manager):
	pass


class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')#with the related_name here we can use userProfile.profile.followed_by.county insted of userProfile.user.followed_by.count
	name = models.CharField(max_length=200, null=True)
	phone = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200, null=True)
	profile_pic = models.ImageField(default="default.png", null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	following   = models.ManyToManyField(User, blank=True, related_name='followed_by')
	# user.profile.following -- users i follow
	# user.followed_by -- users that follow me -- reverse relationship
	slug = models.SlugField(blank=True, null=True)


	def save(self , *args , **kwargs):
		if not self.slug and self.name :
			self.slug = slugify(self.name)
		super(Profile , self).save(*args , **kwargs)

	objects = UserProfileManager()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Profile"
		verbose_name_plural = "Profiles"

	def get_following(self):
		users  = self.following.all()
		return users.exclude(username=self.user.username)

	def get_followors(self):
		users  = self.user.followed_by.all()
		return users.exclude(user=self.user)
