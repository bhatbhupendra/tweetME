from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import CreateUserForm, UserProfileForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#@login_required(login_url='login')
from .decorators import unauthenticated_user

# Create your views here.
@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)
			return redirect('accounts:login')


	content = {'form':form}
	return render(request, 'register.html', content)

@unauthenticated_user
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home:tweetList')
		else:
			messages.info(request, 'Username OR password is incorrect')
	content = {}
	return render(request, 'login.html', content)

@login_required(login_url='accounts:login')
def logoutUser(request):
	logout(request)
	return redirect('accounts:login')

@login_required(login_url='accounts:login')
def userPage(request, slug):
	user_profile = Profile.objects.get(slug=slug)

	tweets = user_profile.tweets_set.all().order_by("-timestamp") #user tweets_set

	#follow check--------------------------------------------------------------
	toggle_user = get_object_or_404(Profile, slug__iexact=slug)
	profile, created = Profile.objects.get_or_create(user=request.user) #or user_profile=request.user
	if toggle_user.user in profile.following.all():
		follow = True
	else:
		follow = False

	content = {
		'user_profile' : user_profile,
		'tweets' : tweets,
		'follow': follow,
	}
	return render(request, 'user.html', content)


@login_required(login_url='accounts:login')
def accountSettings(request):
	profile = request.user.profile
	form = UserProfileForm(instance=profile)

	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()


	content = {
		'form':form
		}

	return render(request, 'settings.html', content)



@login_required(login_url='accounts:login')
def follow(request,slug):
	toggle_user = get_object_or_404(Profile, slug__iexact=slug)
	if request.user.is_authenticated:
		user_profile, created = Profile.objects.get_or_create(user=request.user) #or user_profile=request.user
		if toggle_user.user in user_profile.following.all():
			user_profile.following.remove(toggle_user.user)
		else:
			user_profile.following.add(toggle_user.user)


	return redirect('accounts:userPage', slug)
