from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

class Movie:
    def __init__(self, title, genre, rating):
        self.title = title
        self.genre = genre
        self.rating = rating

class MovieRecommendationSystem:
    def __init__(self):
        self.movies = []

    def add_movie(self, title, genre, rating):
        movie = Movie(title, genre, rating)
        self.movies.append(movie)

    def search_movies_by_title(self, title):
        return [movie for movie in self.movies if title.lower() in movie.title.lower()]

    def search_movies_by_genre(self, genre):
        return [movie for movie in self.movies if genre.lower() in movie.genre.lower()]

    def delete_movie(self, title):
        self.movies = [movie for movie in self.movies if movie.title.lower() != title.lower()]

    def recommend_top_n_movies(self, n):
        sorted_movies = sorted(self.movies, key=lambda movie: movie.rating, reverse=True)
        return sorted_movies[:n]

system = MovieRecommendationSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_movie', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        rating = float(request.form['rating'])
        system.add_movie(title, genre, rating)
        return redirect(url_for('index'))
    return render_template('add_movie.html')

@app.route('/search_movie', methods=['GET', 'POST'])
def search_movie():
    movies = []
    if request.method == 'POST':
        search_by = request.form['search_by']
        keyword = request.form['keyword']
        if search_by == 'title':
            movies = system.search_movies_by_title(keyword)
        elif search_by == 'genre':
            movies = system.search_movies_by_genre(keyword)
    return render_template('search_movie.html', movies=movies)

@app.route('/recommend_movie', methods=['GET', 'POST'])
def recommend_movie():
    movies = []
    if request.method == 'POST':
        n = int(request.form['top_n'])
        movies = system.recommend_top_n_movies(n)
    return render_template('recommend_movie.html', movies=movies)

@app.route('/delete_movie', methods=['GET', 'POST'])
def delete_movie():
    if request.method == 'POST':
        title = request.form['title']
        system.delete_movie(title)
        return redirect(url_for('index'))
    return render_template('delete_movie.html')

if __name__ == '__main__':
    app.run(debug=True)
