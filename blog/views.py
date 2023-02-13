
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category, Tag, Comments
from django.utils import timezone
from .forms import PostForm, CommentForm, LoginForm, SignUpForm, CategoryForm, ProfileForm
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv
from .models import MyUser

# Create your views here.


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    # posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})


def post_detail(request, slug):
    post = Post.objects.filter(slug=slug).last()
    comment = Comments.objects.filter(post=post, reply__isnull=True).all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply_obj = None
            try:
                reply_id = int(request.POST.get('reply_id'))
            except:
                reply_id = None
            if reply_id:
                reply_obj = Comments.objects.get(id=reply_id)
                if reply_obj:
                    reply_comment = form.save(commit=False)
                    reply_comment.reply = reply_obj
            
            
            new_comment = form.save(commit=False)
            new_comment.post=post
            new_comment.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()
        post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comments': comment})


def category_detail(request, id):
    category = Category.objects.filter(id=id).last()
    print(category,'cccccccccccccc')
    posts = Post.objects.filter(category=category).all()
    return render(request, 'blog/post_list.html', {'posts': posts})

# def tag_detail(request, pk):
#     tag = Tag.objects.filter(id=pk).last()
#     posts = Post.objects.filter(tag__name=tag).all()
#     return render(request, 'blog/tag_detail.html', {'posts': posts})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            form.save_m2m()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def signup(request):
    if request.user.is_authenticated:
        return redirect('blog:post_list')
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('blog:post_list')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                auth_login(request,user)
                return redirect('blog:post_list')
            else:
                messages.error(request,'Invalid Credential')
                return redirect('login')
    form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('blog:post_list')


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tag_list.html', {'tags': tags})


def tag_detail(request, slug):
    tag = Tag.objects.filter(id=slug).last()
    posts = Post.objects.filter(tag__name=tag).all()
    return render(request, 'blog/tag_detail.html', {'posts': posts})

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request,'blog/add_category.html', {'form':form})




def user_profile(request):
    form = ProfileForm(None,instance=request.user)
    # print(MyUser.objects.get(request.user))
    return render(request,'blog/user_profile.html', {'form': form})
    

def profile_edit(request):
    form = ProfileForm(None,instance=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile Updated')
            return redirect('blog:post_list')
    return render(request,'blog/profile_detail.html', {'form': form})

# def export_csv(request):
#     form = ProfileForm(instance=request.user)
#     response = HttpResponse('text/csv')
#     response['Content-Disposition']= 'attachment; filename=user.csv'
#     writer = csv.writer(response)
#     writer.writerow(['username','first_name','last_name','city'])
#     users = form.values_list('username','first_name','last_name','city')
#     for user in users:
#         writer.writerow(user)
#     return response