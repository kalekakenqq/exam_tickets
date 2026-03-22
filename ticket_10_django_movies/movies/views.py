from django.shortcuts import render
from .models import Movie


def movie_list(request):
    # фильтрация по рейтингу через get-параметр
    min_rating = request.GET.get('min_rating')
    movies = Movie.objects.all()
    if min_rating:
        try:
            movies = movies.filter(rating__gte=float(min_rating))
        except ValueError:
            pass
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'min_rating': min_rating,
    })
