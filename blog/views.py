from .models import Post
from .forms import PostForm
from django.utils import timezone
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic.base import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list_pag(request):
    post_list_p = Post.objects.filter(published=True).order_by('-last_updated')
    paginator = Paginator(post_list_p, 3)

    page = request.GET.get('page')
    try:
        post_pub_p = paginator.page(page)
    except PageNotAnInteger:
        post_pub_p = paginator.page(1)
    except EmptyPage:
        post_pub_p = paginator.page(paginator.num_pages)

    return render(request, 'blog/pagin_post.html', {"post_pub_p": post_pub_p})


def post_list(request):
    posts = Post.objects.filter(published=True).order_by('-last_updated')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_no_show(request):
    if request.user.is_authenticated():
        posts = Post.objects.filter(published=False).order_by('-last_updated')
        return render(request, 'blog/post_no_show.html', {'posts': posts})
    else:
        return HttpResponse('Unauthorized', status=401)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_delete(request, pk):
    if request.user.is_authenticated():
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('Unauthorized', status=401)


def post_new(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            form = PostForm(request.POST)
            # if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.last_updated = timezone.now()
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return HttpResponse('Unauthorized', status=401)


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated():
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            # if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.last_updated = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/post_edit.html', {'form': form})
    else:
        return HttpResponse('Unauthorized', status=401)


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'blog/register.html'

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = 'blog/login.html'
    success_url = '/'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')




