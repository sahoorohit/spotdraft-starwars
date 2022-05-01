from django.urls import reverse
from rest_framework import serializers

from movies.models import Movie
from utils.helpers import get_local_datetime


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'name',
            'is_favorite',
            'release_date',
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = get_local_datetime(instance.created_at)
        representation['updated_at'] = get_local_datetime(instance.updated_at)

        if self.context.get("from_list_view"):
            representation['url'] = self.context["request"].build_absolute_uri(
                reverse("movie_detail", args=(instance.pk,))
            )

        return representation


class MovieFavoriteSerializer(serializers.Serializer):
    custom_name = serializers.CharField(max_length=50, required=False)

    def create(self, validated_data):
        movie = self.context.get('movie')
        movie.is_favorite = True

        custom_name = validated_data.get("custom_name")
        if custom_name:
            movie.custom_name = custom_name

        movie.save(update_fields=["is_favorite", "custom_name", "updated_at"])

        return movie
