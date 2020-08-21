from django.urls import path
from . import views

app_name='tweets'
urlpatterns = [
    path('tweet/<str:pk>/retweet', views.retweetView, name="retweet"),
    path('tweet/<str:pk>/liked', views.likeView, name="liked"),

    path('', views.tweetList, name="tweetList"),
    path('tweet/<str:pk>', views.tweetDetail, name="tweetDetail"),
    path('update/<str:pk>', views.tweetUpdate, name="tweetUpdate"),
    path('delete/<str:pk>', views.tweetDelete, name="tweetDelete"),
]
