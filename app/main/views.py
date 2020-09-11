from flask import render_template,request,redirect,url_for
from . import main
from ..request import get_movies,get_movie,search_movie
from .forms import ReviewForm
from ..models import Review

@main.route('/')
def index():
    popular_movie = get_movie('popular')
    upcoming_movie = get_movie('upcoming')
    now_showing_movie = get_movie('now_playing')
    name = 'Abzedizo'
    title = 'Home - Welcome to The best Movie Review Website Online'
    
    search_movie = request.args.get('movie_query')
    
    if search_movie:
        return redirect(url_for('.search',movie_name=search_movie))
    else:
        return render_template('index.html', name=name, title=title, popular = popular_movie, upcoming = upcoming_movie, now_showing = now_showing_movie )

@main.route('/movie/<int:id>')
def movie(id):
    movie = get_movies(id)
    title = f'{movie.title}'
    reviews = Review.get_reviews(movie.id)
    return render_template('movie.html', title=title, movie=movie, reviews=reviews)

@main.route('/search/<movie_name>')
def search(movie_name):
    movie_name_list = movie_name.split(' ')
    movie_name_format = '+'.join(movie_name_list)
    searched_movie = search_movie(movie_name_format)
    title = f'search results for {movie_name}'
    return render_template('search.html', movie=searched_movie)

@main.route('/movie/review/new/<int:id>', methods=['GET','POST'])
def new_review(id):
    form = ReviewForm()
    movie = get_movies(id)
    
    if form.validate_on_submit():
        title = form.title.data
        review = form.review.data
        new_review = Review(movie.id, title, movie.poster, review)
        new_review.save_review()
        return redirect(url_for('.movie',id=movie.id))
    
    title = f'{movie.title} review'
    return render_template('new_review.html',title = title, review_form=form, movie=movie)