from django.contrib import admin

from movies.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'custom_name',
        'is_favorite',
        'created_at',
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    fields = list_display + ["release_date"]
