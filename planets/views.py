from django.http.request import HttpRequest
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView

from planets.models import Planet
from planets.serializers import PlanetFavoriteSerializer, PlanetSerializer


class PlanetView(APIView):

    def get(self, request: HttpRequest) -> JsonResponse:
        filter_by_fields = {}
        filter_by_name = request.GET.get('name')
        if filter_by_name:
            filter_by_fields["name__icontains"] = filter_by_name

        planets = Planet.objects.filter(**filter_by_fields)
        planet_serializer = PlanetSerializer(
            planets,
            many=True,
            context={'request': request, "from_list_view": True}
        )

        data = {
            "msg": "Planet list fetched successfully." if planet_serializer.data else "Empty planet list.",
            "planets": planet_serializer.data,
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)

    def post(self, request: HttpRequest) -> JsonResponse:
        planet_serializer = PlanetSerializer(data=request.POST)
        planet_serializer.is_valid(raise_exception=True)
        planet_serializer.save()
        data = {
            "msg": "Planet created successfully.",
            "planets": planet_serializer.data,
        }
        return JsonResponse(status=status.HTTP_201_CREATED, data=data)


class PlanetDetailView(APIView):

    def get(self, request: HttpRequest, id: str) -> JsonResponse:
        planet = get_object_or_404(Planet, id=id)
        planet_serializer = PlanetSerializer(planet)
        data = {
            "msg": "Planet details fetched successfully.",
            "details": planet_serializer.data,
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)


class PlanetFavoriteView(APIView):

    def post(self, request: HttpRequest, id: str) -> JsonResponse:
        planet = get_object_or_404(Planet, id=id)
        planet_serializer = PlanetFavoriteSerializer(data=request.POST, context={'planet': planet})
        planet_serializer.is_valid(raise_exception=True)
        planet_serializer.save()
        data = {
            "msg": "Favorite planet added.",
            "details": planet_serializer.data,
        }
        return JsonResponse(status=status.HTTP_200_OK, data=data)
