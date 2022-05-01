from django.urls import re_path

from movies.views import MovieDetailView, MovieFavoriteView, MovieView

urlpatterns = [
    re_path(r'(?P<id>[0-9]+)/favorite/', MovieFavoriteView.as_view(), name="movie_favorite"),
    re_path(r'(?P<id>[0-9]+)/', MovieDetailView.as_view(), name="movie_detail"),
    re_path(r'', MovieView.as_view(), name="movies_list"),
]
