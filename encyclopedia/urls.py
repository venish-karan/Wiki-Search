from django.urls import path
from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>/", views.wiki_title, name="wiki_title"),
    path("wiki/new_page/<str:title>", views.wiki_title, name="new_page_title"),
    path("wiki/new_page",views.new_page, name="new_page"),
    path("wiki/random_page", views.random_page, name="RandomPage"),
]