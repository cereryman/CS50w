from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("<int:auction_id>", views.auction, name="auction"),
    path("add_comment/<int:auction_id>", views.add_comment, name="add_comment"),
    path("add_rem_watchlist/<int:auction_id>", views.add_rem_watchlist, name="add_rem_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("bid/<int:auction_id>", views.bid, name="bid"),
    path("close/<int:auction_id>", views.close, name="close")
]
