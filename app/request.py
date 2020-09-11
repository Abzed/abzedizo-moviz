import urllib.request,json
from .models import Movie

api_key = None

base_url = None

def configure_request(app):
    global api_key, base_url 
    api_key = app.config['MOVIE_API_KEY']
    base_url = app.config['MOVIE_API_BASE_URL']

def get_movie(category):
    get_movie_url = base_url.format(category,api_key)
    
    with urllib.request.urlopen(get_movie_url) as url:
        get_movie_data = url.read()
        get_movie_response = json.loads(get_movie_data)
        
        movie_result = None
        
        if get_movie_response['results']:
            movie_result_list = get_movie_response['results']
            movie_result = process_results(movie_result_list)
            
    return movie_result

def process_results(movie_list):
    movie_result = []
    for movie_items in movie_list:
        id = movie_items.get('id')
        title = movie_items.get('original_title')
        overview = movie_items.get('overview')
        poster = movie_items.get('poster_path')
        vote_average = movie_items.get('vote_average')
        vote_count = movie_items.get('vote_count')
        
        if poster:
            movie_object = Movie(id, title, overview, poster, vote_average, vote_count)
            movie_result.append(movie_object)
            
    return movie_result

def get_movies(id):
    get_movie_details_url = base_url.format(id,api_key)
    
    with urllib.request.urlopen(get_movie_details_url) as url:
        movie_details_data = url.read()
        movie_details_response = json.loads(movie_details_data)

        movie_object = None
        if movie_details_response:
            id = movie_details_response.get('id')
            title = movie_details_response.get('original_title')
            overview = movie_details_response.get('overview')
            poster = movie_details_response.get('poster_path')
            vote_average = movie_details_response.get('vote_average')
            vote_count = movie_details_response.get('vote_count')

            movie_object = Movie(id,title,overview,poster,vote_average,vote_count)

    return movie_object

def search_movie(movie_name):
    search_movie_url = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(api_key,movie_name)
    with urllib.request.urlopen(search_movie_url) as url:
        search_movie_data = url.read()
        search_movie_response = json.loads(search_movie_data)

        search_movie_results = None

        if search_movie_response['results']:
            search_movie_list = search_movie_response['results']
            search_movie_results = process_results(search_movie_list)
        else:
            return []


    return search_movie_results

