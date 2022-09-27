from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from posts.forms import PostCreateForm
from django.views import View
from posts import models
from django.http import HttpResponseNotAllowed, HttpResponseNotFound
# from datetime import datetime
import datetime
from faker import Faker
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from .forms import PostCreateForm, PostModelForms
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from posts import models
# Fake


def fake_create_user(request):
    f = Faker('ru_RU')
    for i in range(100):
        print(i)
        p = f.profile()
        User.objects.create(
            username=p['username'],
            email=p['mail'],
            password=f.password(length=8)
        )
    return redirect('/')


# просто фэйк
# def fake_create_posts(request):
#     f = Faker('ru_RU')
#     users = User.objects.all()
#     for u in users:
#         for i in range(1000):
#             models.Post.objects.create(
#                 title=f.sentence(nb_words=5),
#                 content=f.sentence(nb_words=10),
#                 date=f.date_time_between(),
#                 user=u
#             )
#     return redirect('/')

# фэйк с bulk
def fake_create_posts(request):
    f = Faker('ru_RU')
    users = User.objects.all()
    for u in users:
        models.Post.objects.bulk_create([models.Post(
                title=f.sentence(nb_words=5),
                content=f.sentence(nb_words=10),
                date=f.date_time_between(),
                user=u
            ) for _ in range(10000)])
    return redirect('/')


def profile(request, user_name):
    try:
        user_profile = models.Profile.objects.get(user__username=user_name)
        posts_profile = models.Post.objects.filter(user__username=user_name)
        return render(request, 'registration/profile.html', {'user': user_profile, 'posts': posts_profile})
    except (User.DoesNotExist, models.Profile.DoesNotExist):
        return redirect('/')

# Create your views here.


def home(request):
    # print(request.user)
    return render(request, 'posts/base.html')


# def show_posts(request, post_id: str = None):
#     if request.GET.get('search'):
#         s = request.GET['search']
#         posts_ = list(models.Post.objects.filter(title__contains=s))
#         posts_ += list(models.Post.objects.filter(content__contains=s).exclude(title__contains=s))
#     else:
#         posts_ = models.Post.objects.all()
#         print('all_posts', len(posts_))
#     return render(request, 'posts/posts.html', {'posts': posts_, 'search_str': request.GET.get('search', '')})


def show_posts(request):
    posts_limit = 50

    try:
        p = int(request.GET.get('p',1))
    except ValueError:
        p = 1

    if request.GET.get('d'):
        date = datetime.datetime.strptime(request.GET['d'], '%Y-%m-%d')
        date_to = date + datetime.timedelta(days=1)
        date_query = (Q(date__gte=date) & Q(date__lt=date_to))

    else:
        date_query =Q()

    if request.GET.get('s'):
        s = request.GET['s']

        q1 = models.Post.objects.filter(
            date_query & Q(title__contains=s) & ~Q(content__contains=s)
        ).order_by('-date')

        print(q1.query)

        q2 = models.Post.objects.filter(
            date_query & ~Q(title__contains=s) & Q(content__contains=s)
        ).order_by('-date')

        pages = Paginator(list(q1) + list(q2), posts_limit)

    else:
        q = models.Post.objects.filter(date_query).order_by('-date').all()
        print(q.query)
        pages = Paginator(q, posts_limit)

    if p > pages.num_pages:
        p = pages.num_pages
    if p < 1:
        p = 1

    # print(pages.count)
    return render(
        request, 'posts/posts.html',
        {
            'posts': pages.page(p),
            'search_str' : request.GET.get('s', ''),
            'page' : p,
            'num_pages': int(pages.num_pages),
        }
    )


@transaction.atomic
def update_post(request, post_id):
    print('UPDATE FUNC')
    try:
        user_post = models.Post.objects.get(id=post_id)

        if request.user != user_post.user and not request.user.is_superuser: #нельзя редактировать пост другого пользователя

            return HttpResponseNotAllowed(request)

    except models.Post.DoesNotExist:
        return HttpResponseNotFound(request)

    if request.method == 'GET':
        return render(request, 'posts/create.html',
                      {'title': user_post.title, 'content': user_post.content, 'delete': True, 'post_id': post_id})

    elif request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title') or ''
        content = request.POST.get('content') or ''
        if title and content:
            update_fields = []
            if user_post.title != title:
                update_fields.append('title')
                user_post.title = title

            if user_post.content != content:
                update_fields.append('content')
                user_post.content = content
                # user_post.date = datetime.now()
            with transaction.atomic():
                user_post.save(update_fields=update_fields or None)

            return redirect('/posts')
        else:
            error = 'Укажите все поля'
            return render(request, 'posts/create.html',
                          {'title': title, 'content': content, 'error': error, 'delete': True, 'post_id': post_id})


def post(request, post_id):
    try:
        user_post = models.Post.objects.get(id=post_id)
        author = user_post.user.username

        return render(request, 'posts/user_post.html', {'post': user_post, 'user': author})
    except models.Post.DoesNotExist:
        return HttpResponseNotFound(request)


def about(request):
    return render(request, 'posts/about.html', {'content': '<h1>About</h1>'})


def delete(request, post_id):

    if request.method == 'POST':
        models.Post.objects.get(id=post_id).delete()
        return redirect('/posts/')
    else:
        return HttpResponseNotAllowed(request)


# def delete(request, post_id):
#     post = Post.objects.get()
#     post.delete()
#     # messages = [f'"{post.title}" was successfully deleted!']
#     return redirect('home')




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


# class CreateView(View):
#
#     def get(self, request):
#         print(request.GET)
#         return render(request, 'posts/create.html')
#
#     def post(self, request, user_form=None):
#         print(request.POST)
#         if request.method == 'GET':
#             return render(request, 'posts/create.html', {'form': user_form, 'qwert': 'asdfdsad'})
#         elif request.method == 'POST':
#             user_form = CreateForm(request.POST)
#             if user_form.is_valid():
#                 return redirect('/')
#             return render(request, 'posts/create.html', {'form': user_form})
#
#         return render(request, 'posts/create.html', {'form': user_form})


def create_post(request, user=None):
    user_form = PostModelForms()
    print('CREATE FUNC')

    if request.method == 'GET':
        return render(request, 'posts/create_2.html', {'form': user_form})

    elif request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title') or ''
        content = request.POST.get('content') or ''
        user_form = PostModelForms(request.POST, request.FILES)

        # if title and content:
        if user_form.is_valid():
            post_ = user_form.save(commit=False)
            post_.user = User.objects.get(username=request.user.username)
            post_.save()
            return redirect('/posts')
        else:
            # error = 'Укажите все поля'
            return render(request, 'posts/create_2.html', {'form' : user_form})#{'title': title, 'content': content, 'error': error})


class PostCreateView(CreateView):
    model = models.Post
    form_class = PostModelForms
    success_url = '/'
    template_name = 'posts/create_2.html'

    def form_valid(self, form):
        post_ = form.save(commit=False)
        post_.user = User.objects.get(username=self.request.user.username)
        post_.save()
        return super(PostCreateView, self).form_valid(form)






#было так пока не начали делать формы
# def create_post(request, user=None):
#     user_form = PostModelForms()
#     print('CREATE FUNC')
#
#     if request.method == 'GET':
#         return render(request, 'posts/create_2.html', {'form': user_form})
#
#     elif request.method == 'POST':
#         print(request.POST)
#         title = request.POST.get('title') or ''
#         content = request.POST.get('content') or ''
#         user_form = PostCreateForm(request.POST, request.FILES)
#
#         # if title and content:
#         if user_form.is_valid():
#             # user_post = models.Post(title=request.POST['title'], content=request.POST['content'])
#             # user_post.save()
#             models.Post.objects.create(
#                 # title=title,
#                 title=user_form.cleaned_data['title'],
#                 # content=content,
#                 content=user_form.cleaned_data['content'],
#                 image=user_form.cleaned_data['image'],
#                 user=User.objects.get(username=request.user.username))
#             return redirect('/posts')
#         else:
#             # error = 'Укажите все поля'
#             return render(request, 'posts/create_2.html', {'form' : user_form})#{'title': title, 'content': content, 'error': error})