from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms # Needed for django built-in forms
from django.core.paginator import Paginator # Needed to split posts
from django.contrib.auth.decorators import login_required # Needed for login only views
from django.views.decorators.csrf import csrf_exempt #Needed for JSON put requests
from django.http import JsonResponse #Needed for JSON put requests
import json #Needed for JSON put requests
from .models import User, Post, Follow

# Form to create a new auction
class NewPostForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={'class' : 'textarea'}), max_length=280, label="")

# http://rasmusrasmussen.com/rtweets/ used to generate random posts

def index(request):
    # If post, save to DB and redirect to the all post page
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = NewPostForm(request.POST)

        # Check if form data is valid (server-side)
        if form.is_valid():

            # Isolate the items from the 'cleaned' version of form data
            body = form.cleaned_data["body"]
            user = request.user
            # Write to DB, post table only if user is authenticated
            if request.user.is_authenticated:
                post = Post(user=user, body=body)
                post.save()
            else:
                pass

        return HttpResponseRedirect(reverse("index"))
    # Else, display the all post page
    else:
        post_list = Post.objects.all().order_by('-timestamp')

        # Paginate
        paginator = Paginator(post_list, 10) # Show 10 posts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, "network/index.html", {
            "newpostform": NewPostForm(),
            "page_obj": page_obj
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, user_id):
    # Get the user ID and extract post list
    user = User.objects.get(id=user_id)
    post_list = Post.objects.filter(user=user).order_by('-timestamp')

    # Paginate
    paginator = Paginator(post_list, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Show # of followers and following
    followers = Follow.objects.filter(following=user_id).count()
    following = Follow.objects.filter(follower=user_id).count()

    # Check if the current user can follow/unfollowing the viewed user.
    if request.user.is_authenticated:
        follow_status = Follow.objects.filter(following=User.objects.get(id=user_id)).filter(follower=User.objects.get(id=request.user.id))
    else:
        follow_status = 0

    return render(request, "network/profile.html", {
        "profile": user,
        "header": "Profile",
        "page_obj": page_obj,
        "followers": followers,
        "following": following,
        "follow_status": follow_status
    })

@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def follow(request, user_id):
    following = User.objects.get(id=user_id)
    follower =  User.objects.get(id=request.user.id)

    follow = Follow.objects.filter(following=following).filter(follower=follower)

    if follower != following:
        if follow:
            # Write to DB, follow table
            follow.delete()
        else:
            # Write to DB, follow table
            follow = Follow(following=following, follower=follower)
            follow.save()

    return HttpResponseRedirect(reverse("profile", args=(user_id)))


@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def following(request):
    # Extract posts from followed users.
    # credit to https://stackoverflow.com/questions/53803106/django-query-how-to-find-all-posts-from-people-you-follow for this query
    post_list = Post.objects.filter(user__following__follower__id=request.user.id).order_by('-timestamp')

    # Paginate
    paginator = Paginator(post_list, 10) # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html", {
    "page_obj": page_obj,
    })

@csrf_exempt
@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def like(request, post_id):
    # Implement as a HTTP response so that page doesn't refresh

    # Composing a new email must be via PUT
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Get the post and uer ID
    post = Post.objects.get(id=post_id)
    liker =  User.objects.get(id=request.user.id)

    # If the user likes, remove like, else add like
    if liker in post.like.all():
        # Write to DB, post table
        post.like.remove(liker)
    else:
        # Write to DB, post table
        post.like.add(liker)

    return HttpResponse(status=204)



@csrf_exempt
@login_required(login_url='login') # From https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
def edit(request, post_id):
    # Editing a post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Extract Post ID and data
    post = Post.objects.get(pk=post_id)
    data = json.loads(request.body)
    body = data.get("body", "")

    # Ensure that only the owner of the post can edit it.
    owner = Post.objects.get(pk=post_id).user.id
    editor = User.objects.get(id=request.user.id).id

    if owner == editor:
        post.body = body
        post.save()
        return JsonResponse({"message": "Post edited successfully."}, status=201)
    else:
        return JsonResponse({"message": "Permission denied!"}, status=500)

