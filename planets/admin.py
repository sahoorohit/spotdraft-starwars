from django.contrib import admin

from planets.models import Planet


@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'custom_name',
        'is_favorite',
        'created_at',
    ]
    readonly_fields = ['id', 'created_at', 'updated_at']
    fields = list_display
