from django.shortcuts import render, HttpResponse

# Create your views here.


def home(request):
    return render(request, 'posts/base.html')


def posts(request):
    post_content = request.headers
    return render(request, 'posts/posts.html', {'content': post_content})


def about(request):
    return render(request, 'posts/about.html', {'content': '<h1>About</h1>'})
