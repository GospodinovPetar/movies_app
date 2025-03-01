from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Movie
from .utils import generate_movie, TMDB_API_KEY, TMDB_BASE_URL


def movie_list(request):
    """
    Displays movies ordered by newest first (i.e. descending by id) with pagination (5 movies per page),
    along with any recommended movie.
    """
    movies = Movie.objects.all().order_by('-id')  # Newest movies first
    paginator = Paginator(movies, 3)  # 3 movies per page

    page = request.GET.get('page')
    try:
        movies_page = paginator.page(page)
    except PageNotAnInteger:
        movies_page = paginator.page(1)
    except EmptyPage:
        movies_page = paginator.page(paginator.num_pages)

    recommended = request.session.get("recommended_movie", None)
    return render(request, "movies.html", {"movies": movies_page, "recommended_movie": recommended})


def add_movie_to_list(request):
    """
    Adds the recommended movie to the database.
    It fetches detailed genre information from TMDb using the stored tmdb_id,
    and then saves the movie with up to three genres.
    Only the primary genre (first genre from TMDb) is mandatory.
    """
    recommended = request.session.get("recommended_movie", None)

    if recommended:

        tmdb_id = recommended.get("tmdb_id")

        if not tmdb_id:
            return redirect("movie_list")

        # Fetch full movie details from TMDb
        resp = requests.get(f"https://api.themoviedb.org/3/movie/{tmdb_id}",
                            params={"api_key": TMDB_API_KEY})

        if resp.status_code != 200:
            return redirect("movie_list")

        details = resp.json()
        genres = [g["name"] for g in details.get("genres", [])]
        primary_genre = genres[0] if genres else ""
        secondary_genre = genres[1] if len(genres) > 1 else ""
        third_genre = genres[2] if len(genres) > 2 else ""

        # Add the movie only if it doesn't already exist
        if not Movie.objects.filter(title=recommended["title"]).exists():
            Movie.objects.create(
                title=recommended["title"],
                primary_genre=primary_genre,
                secondary_genre=secondary_genre,
                third_genre=third_genre,
                year=recommended["year"],
                description=recommended["overview"]
            )

        # Remove recommendation from session after adding
        request.session.pop("recommended_movie", None)

    return redirect("movie_list")


def generate_movie_view(request):
    """
    View to generate a recommended movie.
    """
    generate_movie(request)
    return redirect("movie_list")


def delete_movie(request, movie_id):
    """
    Deletes a movie from the database.
    """
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect("movie_list")


def edit_movie(request, movie_id):
    """
    Edit an existing movie's details.
    """
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        movie.title = request.POST.get("title")
        movie.primary_genre = request.POST.get("primary_genre")
        movie.secondary_genre = request.POST.get("secondary_genre") or ""
        movie.third_genre = request.POST.get("third_genre") or ""
        movie.year = int(request.POST.get("year"))
        movie.description = request.POST.get("description")
        movie.save()
        return redirect("movie_list")

    return render(request, "edit_movie.html", {"movie": movie})


def add_movie_view(request):
    """
    Allows the user to add a movie by entering only the movie title.
    The view searches TMDb for the movie, fetches full details (including genres),
    and then saves the movie to the database.
    """
    if request.method == "POST":
        movie_title = request.POST.get("title", "").strip()
        if not movie_title:
            return render(request, "add_movie.html", {"error": "Please enter a movie title."})

        # Check if the movie already exists (case-insensitive)
        if Movie.objects.filter(title__iexact=movie_title).exists():
            return render(request, "add_movie.html", {"error": "Movie already exists in the database."})

        # Search for the movie on TMDb
        search_url = f"{TMDB_BASE_URL}/search/movie"
        search_params = {
            "api_key": TMDB_API_KEY,
            "query": movie_title,
            "language": "en-US",
            "include_adult": "false"
        }

        search_resp = requests.get(search_url, params=search_params)
        if search_resp.status_code != 200:
            return render(request, "add_movie.html", {"error": "Error contacting TMDb."})

        results = search_resp.json().get("results", [])

        if not results:
            return render(request, "add_movie.html", {"error": "No movie found with that title."})

        # Use the first result as the best match
        best_match = results[0]
        tmdb_id = best_match.get("id")

        # Fetch full movie details from TMDb
        details_url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
        details_params = {"api_key": TMDB_API_KEY, "language": "en-US"}
        details_resp = requests.get(details_url, params=details_params)

        if details_resp.status_code != 200:
            return render(request, "add_movie.html", {"error": "Error fetching movie details from TMDb."})
        details = details_resp.json()

        # Extract movie details
        title = details.get("title")
        release_date = details.get("release_date", "Unknown")
        year = release_date.split("-")[0] if release_date != "Unknown" and release_date else 0
        overview = details.get("overview", "")

        # Extract genres from TMDb details (TMDb returns a list of dictionaries)
        genres = details.get("genres", [])
        primary_genre = genres[0]["name"] if len(genres) > 0 else ""
        secondary_genre = genres[1]["name"] if len(genres) > 1 else ""
        third_genre = genres[2]["name"] if len(genres) > 2 else ""

        # Create the movie in our database
        Movie.objects.create(
            title = title,
            primary_genre = primary_genre,
            secondary_genre = secondary_genre,
            third_genre = third_genre,
            year = int(year) if isinstance(year, str) and year.isdigit() else (year if isinstance(year, int) else 0),
            description = overview
        )

        return redirect("movie_list")

    # For GET requests, display the simple form
    return render(request, "add_movie.html")