from django.urls import re_path

from planets.views import PlanetDetailView, PlanetFavoriteView, PlanetView

urlpatterns = [
    re_path(r'(?P<id>[0-9]+)/favorite/', PlanetFavoriteView.as_view(), name="planet_favorite"),
    re_path(r'(?P<id>[0-9]+)/', PlanetDetailView.as_view(), name="planet_detail"),
    re_path(r'', PlanetView.as_view(), name="planets_list"),
]
