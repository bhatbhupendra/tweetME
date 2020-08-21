from django.urls import path
from . import views

app_name='hashtag'
urlpatterns = [
    path('<slug:tag>/', views.hashTagView, name="hashtag"),
]
