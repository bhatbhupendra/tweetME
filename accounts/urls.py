from django.urls import path
from . import views

app_name='accounts'
urlpatterns = [
    path('register', views.registerPage, name="register"),
	path('login', views.loginPage, name="login"),
	path('logout', views.logoutUser, name="logout"),

    path('user/<slug:slug>', views.userPage, name="userPage"),
    path('account', views.accountSettings, name="accountSettings"),

    path('follow/<slug:slug>', views.follow, name="follow"),#http://localhost:8000/accounts/user/2/follow
]
