
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user_id>", views.profile, name="profile"),
    path("follow/<str:user_id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("like/<str:post_id>", views.like, name="like"),
    path("edit/<str:post_id>", views.edit, name="edit")
]
