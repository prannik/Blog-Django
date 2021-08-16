from django.shortcuts import render, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from .models import Post
from .forms import SigUpForm, SignInForm, FeedBackForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q


class MainView(View):
    def get(self, request):
        posts = Post.objects.all()
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myblog/home.html', context={
            'page_obj': page_obj,
        })

class PostDetailView(View):
    def get(self, request, slug):
        post = get_object_or_404(Post, url=slug)
        return render(request, 'myblog/post_detail.html', context={
            'post': post
        })

class SignUpView(View):
    def get(self, request):
        form = SigUpForm()
        return render(request, 'myblog/signup.html', context={
            'form': form,
        })

    def post(self, request):
        form = SigUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'myblog/signup.html', context={
            'form': form,
        })

class SignInView(View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'myblog/signin.html', context={
            'form': form,
        })

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'myblog/signin.html', context={
            'form': form,
        })

class FeedBackView(View):
    def get(self, request):
        form = FeedBackForm()
        return render(request, 'myblog/contact.html', context={
            'form': form,
            'title': 'Написать мне',
        })

    def post(self, request):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name} | {subject}', message, from_email, ['prannik.m@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Неправильный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'myblog/contact.html', context={
            'form': form
        })

class SuccessView(View):
    def get(self, request):
        return render(request, 'myblog/success.html', context={
            'title': "Большое спасибо",
        })

class SearchResultView(View):

    def get(self, request):
        query = self.request.GET.get('q')
        result = ''
        if query:
            result = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
                | Q(title__icontains=query) | Q(description__icontains=query)
            )
        paginator = Paginator(result, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myblog/search.html', context={
            'title': "Поиск",
            'results': page_obj,
            'count': paginator.count,
        })
