from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("active", views.active, name="active"),
    path("create", views.create, name="create"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("watchlist", views.watchlist, name='watchlist'),
    path("listing/<int:listing_id>", views.list, name="listing"),
    path("close/<int:listing_id>", views.close, name="close"),
    path("watchlist_add/<int:listing_id>", views.watchlist_add, name='watchlist_add'),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("watchlist_remove/<int:listing_id>", views.watchlist_remove, name='watchlist_remove'),
    path("categories", views.categories, name='categories'),
    path('categories/<str:category>/', views.category_page, name='category_page'),
]
