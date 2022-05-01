from django.urls import reverse
from rest_framework import serializers

from planets.models import Planet
from utils.helpers import get_local_datetime


class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = (
            'name',
            'is_favorite',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = get_local_datetime(instance.created_at)
        representation['updated_at'] = get_local_datetime(instance.updated_at)

        if self.context.get("from_list_view"):
            representation['url'] = self.context["request"].build_absolute_uri(
                reverse("planet_detail", args=(instance.pk,))
            )

        return representation


class PlanetFavoriteSerializer(serializers.Serializer):
    custom_name = serializers.CharField(max_length=50, required=False)

    def create(self, validated_data):
        planet = self.context.get('planet')
        planet.is_favorite = True

        custom_name = validated_data.get("custom_name")
        if custom_name:
            planet.custom_name = custom_name

        planet.save(update_fields=["is_favorite", "custom_name", "updated_at"])

        return planet
