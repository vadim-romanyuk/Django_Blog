from django.shortcuts import render, HttpResponse, redirect
from posts.forms import CreateForm
from django.views import View
from posts import models

# Create your views here.


def home(request):
    # print(request.user)
    return render(request, 'posts/base.html')


def show_posts(request, post_id: str = None):
    posts_ = models.Post.objects.all()
    return render(request, 'posts/posts.html', {'posts': posts_})


def update_post(request, post_id):
    print('UPDATE FUNC')
    user_post = models.Post.objects.get(id=post_id)

    if request.method == 'GET':
        return render(request, 'posts/create.html', {'title': user_post.title, 'content': user_post.content, 'delete': True})

    elif request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title') or ''
        content = request.POST.get('content') or ''
        if title and content:
            user_post.title = title
            user_post.content = content
            user_post.save()
            return redirect('/posts')
        else:
            error = 'Укажите все поля'
            return render(request, 'posts/create.html', {'title': title, 'content': content, 'error': error, 'delete': True})


def post(request, post_id):
    user_post = models.Post.objects.get(id=post_id)
    return render(request, 'posts/user_post.html', {'post': user_post})


def about(request):
    return render(request, 'posts/about.html', {'content': '<h1>About</h1>'})

# def create(request):
#     return render(request, 'posts/create.html', {'content': '<h1>Create</h1>'})

# def create_post(request):
#     print('create')
#     user_form = CreateForm()
#
#     if request.method == 'GET':
#         return render(request, 'posts/create.html', {'form': user_form, 'qwert': 'asdfdsad'})
#     elif request.method == 'POST':
#         user_form = CreateForm(request.POST)
#         if user_form.is_valid():
#             return redirect('/')
#         return render(request, 'posts/create.html', {'form': user_form})
#
#     return render(request, 'posts/create.html', {'form': user_form})


class CreateView(View):

    def get(self, request):
        print(request.GET)
        return render(request, 'posts/create.html')

    def post(self, request):
        print(request.POST)
        if request.method == 'GET':
            return render(request, 'posts/create.html', {'form': user_form, 'qwert': 'asdfdsad'})
        elif request.method == 'POST':
            user_form = CreateForm(request.POST)
            if user_form.is_valid():
                return redirect('/')
            return render(request, 'posts/create.html', {'form': user_form})

        return render(request, 'posts/create.html', {'form': user_form})


def create_post(request):
    print('CREATE FUNC')

    if request.method == 'GET':
        return render(request, 'posts/create.html')

    elif request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title') or ''
        content = request.POST.get('content') or ''
        if title and content:
            # user_post = models.Post(title=request.POST['title'], content=request.POST['content'])
            # user_post.save()
            models.Post.objects.create(title=title, content=content)
            return redirect('/')
        else:
            error = 'Укажите все поля'
            return render(request, 'posts/create.html', {'title': title, 'content': content, 'error': error})

