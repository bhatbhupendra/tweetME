from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *
from accounts.models import Profile

from django.db.models import Q

from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='accounts:login')
def tweetList(request):
	user_profile, created = Profile.objects.get_or_create(user=request.user) #or user_profile=request.user
	im_following = user_profile.get_following()

	tweets = Tweets.objects.all()
	#q1 = tweets.filter(tweetUser__user__in=im_following)
	#q2 = tweets.filter(tweetUser__user=im_following)
	tweets=(tweets.filter(tweetUser__user__in=im_following) | tweets.filter(tweetUser=user_profile)).distinct().order_by("-timestamp")

	search_query = request.GET.get('q')
	if search_query:
		tweets = tweets.filter(
			Q(profile__user__username__icontains = search_query)|
			Q(content__icontains= search_query)
		).distinct()

	paginator = Paginator(tweets, 2) # Show 2 posts per page

	page = request.GET.get('page')
	tweets = paginator.get_page(page)

	form = TweetModelForm()
	if request.method == 'POST':
		form = TweetModelForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.tweetUser = request.user.profile
			instance.save()
			return redirect('home:tweetList')

	content = {
		'tweets' : tweets,
		'form' : form,
		'user_profile' : user_profile,
	}
	return render(request, 'tweetList.html', content)

@login_required(login_url='accounts:login')
def tweetDetail(request,pk):
	tweet = Tweets.objects.get(id=pk)
	content = {
		'tweet' : tweet,
	}
	return render(request, 'tweetDetail.html', content)

@login_required(login_url='accounts:login')
def tweetUpdate(request,pk):
	tweet = Tweets.objects.get(id=pk)

	form = TweetModelForm(instance=tweet)
	if request.method == 'POST':
		form = TweetModelForm(request.POST, instance=tweet)
		if form.is_valid():
			form.save()
			return redirect('home:tweetList')

	content = {
		'tweet' : tweet,
		'form': form,
	}
	return render(request, 'tweetUpdate.html', content)

@login_required(login_url='accounts:login')
def tweetDelete(request, pk):
	tweet = Tweets.objects.get(id=pk)
	if request.method == 'POST':
		tweet.delete()
		return redirect('home:tweetList')

	return render(request, 'tweetDelete.html', {'tweet': tweet})

@login_required(login_url='accounts:login')
def retweetView(request, pk):
	tweet = get_object_or_404(Tweets, pk=pk)
	if request.user.is_authenticated:
		newTweet = Tweets.objects.retweet(request.user.profile, tweet)#Tweets.tweetUser must be prifile instinces
	else:
		return redirect('accounts:login')
	return redirect('home:tweetList')


@login_required(login_url='accounts:login')
def likeView(request, pk):
	tweet = get_object_or_404(Tweets, pk=pk)
	if request.user.is_authenticated:
		liked_value = Tweets.objects.liked_toggle(request.user, tweet)
	else:
		return redirect('accounts:login')
	return redirect('home:tweetList')
