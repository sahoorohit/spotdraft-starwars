from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView

from movies.models import Movie
from movies.serializers import MovieFavoriteSerializer, MovieSerializer


class MovieView(APIView):

    def get(self, request: HttpRequest) -> JsonResponse:
        filter_by_fields = {}
        filter_by_name = request.GET.get('name')
        if filter_by_name:
            filter_by_fields["name__icontains"] = filter_by_name

        movies = Movie.objects.filter(**filter_by_fields)
        movie_serializer = MovieSerializer(
            movies,
            many=True,
            context={'request': request, "from_list_view": True}
        )

        data = {
            "msg": "Movie list fetched successfully." if movie_serializer.data else "Empty Movie list.",
            "movies": movie_serializer.data,
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)

    def post(self, request: HttpRequest) -> JsonResponse:
        movie_serializer = MovieSerializer(data=request.POST)
        movie_serializer.is_valid(raise_exception=True)
        movie_serializer.save()
        data = {
            "msg": "Movie created successfully.",
            "details": movie_serializer.data,
        }
        return JsonResponse(status=status.HTTP_201_CREATED, data=data)


class MovieDetailView(APIView):

    def get(self, request: HttpRequest, id: str) -> JsonResponse:
        planet = get_object_or_404(Movie, id=id)
        planet_serializer = MovieSerializer(planet)
        data = {
            "msg": "Movie details fetched successfully.",
            "details": planet_serializer.data,
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


class MovieFavoriteView(APIView):

    def post(self, request: HttpRequest, id: str) -> JsonResponse:
        movie = get_object_or_404(Movie, id=id)
        movie_serializer = MovieFavoriteSerializer(data=request.POST, context={'movie': movie})
        movie_serializer.is_valid(raise_exception=True)
        movie_serializer.save()
        data = {
            "msg": "Favorite movie added.",
            "details": movie_serializer.data,
        }
        return JsonResponse(status=status.HTTP_201_CREATED, data=data)
