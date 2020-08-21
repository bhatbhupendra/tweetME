from django.shortcuts import render

# Create your views here.
from .models import hashtag

def hashTagView(request,tag):
    hash_tag, created = hashtag.objects.get_or_create(tag=tag)
    content = {
        'hash_tag' : hash_tag,
    }
    return render(request, 'hashtag.html', content)
