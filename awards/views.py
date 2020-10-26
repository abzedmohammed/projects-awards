from django.contrib.auth import login, authenticate
from django.shortcuts import render, HttpResponseRedirect, redirect, get_object_or_404
from django.http  import HttpResponse
import datetime as dt
from django.http import HttpResponse, Http404,HttpResponseRedirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.conf import settings 
from django.core.mail import send_mail 
from django.urls import reverse
from django.db import transaction
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
# from next_prev import next_in_order, prev_in_order

@login_required
def index(request):
    post = Project.objects.all()
    first = Project.objects.order_by('?').first()
    # second = next_in_order(first)
    # prev_in_order(second) == first # True
    # last = prev_in_order(first, loop=True)
    return render(request, 'index.html', {'post':post, 'first':first})

@login_required
def single_project(request,post_id):
    post = get_object_or_404(Project, id=post_id)
    # pics = Screenshot.objects.get(project=post_id)
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    comments = Comment.objects.filter(project=post).order_by('-date')
    
    # if request.method == "POST":
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         data = form.save(commit=False)
    #         data.user = user
    #         data.project = post
    #         data.save()
    #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  
    #         #return redirect('singlePost')
    #     else:
    #         form = CommentForm()
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = request.POST.get("comment")
            user = request.user
            project = post
            get_comment = Comment(comment=comment, project=project,profile=profile)
            get_comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = CommentForm()
    
    return render(request, 'awards.html', {'post':post, 'form':CommentForm, 'comments':comments, 
                                           'profile':profile}) 
@login_required
def like(request,post_id):
    user = request.user
    post = Project.objects.get(id=post_id)
    current_likes = post.like
    
    liked = Likes.objects.filter(user=user, project=post).count()
    
    if not liked:
        like = Likes.objects.create(user=user,project=post)
        
        current_likes = current_likes + 1
        
    else:
        Likes.objects.filter(user=user,project=post).delete()
        current_likes = current_likes - 1
        
    post.like = current_likes
    post.save() 
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  

@login_required
def profile_edit(request,username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    form = EditProfileForm(instance=profile)
    
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.save()
            return HttpResponseRedirect(reverse('profile', args=[username]))
        else:
            form = EditProfileForm(instance=profile)
    legend = 'Edit Profile'
    return render(request, 'profile/update.html', {'legend':legend, 'form':EditProfileForm})

@login_required
def follow(request, username, option):
    user = request.user
    folllowing = get_object_or_404(User, username=username)
    
    try:
        f, created = Follow.objects.get_or_create(follower=user, following=folllowing)
        
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=folllowing, user=user).all().delete()
            
        else:
            posts = Project.objects.all().filter(user=folllowing)[:10]
            
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.date, following=folllowing)
                    stream.save()
                    
        return HttpResponseRedirect(reverse('profile', args=[username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args=[username]))      


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)
    skills = Profile.objects.all()
    posts = Project.objects.filter(user=user).order_by("-date")
    
    post_count = Project.objects.filter(user=user).count()
    follower_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()
    follow_status = Follow.objects.filter(following=user, follower=request.user).exists()
    
    return render(request,'profile/profile.html', {'user':user, 'profile':profile, 'posts':posts, 'post_count':post_count, 
                                                   'follower_count':follower_count, 'following_count':following_count,'follow_status':follow_status,
                                                   'skills':skills})

@login_required
def post_project(request):
    userX = request.user
    user = Profile.objects.get(user=request.user)
    
    if request.method == "POST":
        
        form = ProjectForm(request.POST, request.FILES)
        form_s = ScreenshotForm(request.POST, request.FILES)
        
        if form_s.is_valid and form.is_valid():
            data_s = form_s.save()
            data = form.save(commit=False)
            data.profile = user
            data.user = userX
            data.screenshots = data_s
            data.save()
            return redirect('/')
        else:
            return False
    
    return render(request, 'new_post.html', {'form':ProjectForm, 'form_s':ScreenshotForm})


# @login_required
# def search_results(request):
    
#     if "users" in request.GET and request.GET["users"]:
#         search_term = request.GET.get("users")
#         searched_accounts = Post.search_user(search_term)
#         message = f"{search_term}"

#         return render(request, 'search.html',{"message":message,"users": searched_accounts})

#     else:
#         message = "You haven't searched for any user"
#         return render(request, 'search.html',{"message":message})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(request,'/')
    
    return render(request, '/django_registration/login.html')

@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('/')