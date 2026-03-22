from django.contrib import admin
from django.utils.html import format_html
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['title', 'director', 'year', 'rating_display']
    search_fields = ['title']
    list_filter = ['year']

    def rating_display(self, obj):
        # цвет зависит от рейтинга
        if obj.rating >= 8:
            color = 'green'
        elif obj.rating >= 7:
            color = 'orange'
        else:
            color = 'red'
        return format_html('<b style="color:{}">{}</b>', color, obj.rating)

    rating_display.short_description = 'рейтинг'
