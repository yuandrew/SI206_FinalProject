from flask import Flask, render_template, request, redirect
import main
import sqlite3
import plotly.plotly as py
import plotly.graph_objs as go

app = Flask(__name__)
most_popular_list = ['Arts', 'Automobiles', 'Blogs', 'Books', 'Business Day',
    'Education', 'Fashion & Style', 'Food', 'Health', 'Job Market', 'Magazine',
    'membercenter', 'Movies', 'Multimedia', 'NYT Now', 'Obituaries', 'Open',
    'Opinion', 'Public Editor', 'Real Estate', 'Science', 'Sports', 'Style',
    'Sunday Review', 'T Magazine', 'Technology', 'The Upshot', 'Theater',
    'Times Insider', 'Today’s Paper', 'Travel', 'U.S.', 'World', 'Your Money',
    'all-sections']

class Nearby:
    def __init__(self, init_tuple):
        self.name = init_tuple[0]
        self.address = init_tuple[1]
        self.distance = format(init_tuple[2], '.2f')
        self.price = init_tuple[3]
        self.rating = init_tuple[4]
        self.review_count = init_tuple[5]
        self.url = init_tuple[6]
        self.phone = init_tuple[7]
class BestSeller:
    def __init__(self, init_tuple):
        self.title = init_tuple[0]
        self.author = init_tuple[1]
        self.created_date = init_tuple[2]
        self.primary_isbn13 = init_tuple[3]
        self.age = init_tuple[4]
        self.description = init_tuple[5]
class MostPopular:
    def __init__(self, init_tuple):
        self.title = init_tuple[0]
        self.url = init_tuple[1]
        self.published_date = init_tuple[2]
        self.abstract = init_tuple[3]

@app.route('/')
def home():
    main.program_start()
    return render_template('home.html')



@app.route('/select', methods=['POST'])
def signup():
    search_type = request.form['search_type']
    return redirect('/' + search_type)

@app.route('/restaurantsearch')
def restaurant_search():
    return render_template('restaurant.html')

@app.route('/restaurantsearch/confirm', methods=['POST'])
def restaurant_search_confirm():
    location = request.form['location']
    main.map_nearby_search(location)
    return redirect('/restaurantsearch/results')

@app.route('/restaurantsearch/results')
def restaurant_search_nearby():
    conn = sqlite3.connect(main.DBNAME)
    cur = conn.cursor()
    statement = '''SELECT search_address FROM Gmap'''
    cur.execute(statement)
    search = ''
    for row in cur:
        if search == '':
            search = row[0]
    statement = '''
        SELECT ?, ?, ?, ?, ?, ?, ?, ?
        FROM Gmap
        JOIN Yelp
        ON Yelp.name=GMap.name'''
    insert = ('GMap.name', 'GMap.address', 'distance', 'price', 'rating',
                'review_count', 'url', 'phone')
    cur.execute(statement, insert)
    search_result = []
    for row in cur:
        search_result.append(Nearby(row))
    return render_template('restaurant_nearby.html', result=search_result, place=search)



@app.route('/bestsellers')
def best_sellers():
    return render_template('bestsellers.html')

@app.route('/bestsellers/confirm', methods=['POST'])
def bs_search():
    date = request.form['date']
    main.nyt_book_search(date)
    return redirect('/bestsellers/results')

@app.route('/bestsellers/results')
def best_sellers_result():
    conn = sqlite3.connect(main.DBNAME)
    cur = conn.cursor()
    statement = 'SELECT ?, ?, ?, ?, ?, ? FROM Books'
    insert = ('title', 'author', 'created_date', 'primary_isbn13',
                'age_group', 'description')
    cur.execute(statement, insert)
    search_result = []
    for row in cur:
        search_result.append(BestSeller(row))
    return render_template('bestsellers_result.html', result=search_result)



@app.route('/mostpopular')
def most_popular():
    return render_template('mostpopular.html', list=most_popular_list)

@app.route('/mostpopular/confirm', methods=['POST'])
def mp_search():
    category = request.form['category']
    time = request.form['time']
    main.nyt_mostpopular_search(category, time)
    return redirect('/mostpopular/results')

@app.route('/mostpopular/results')
def most_popular_results():
    conn = sqlite3.connect(main.DBNAME)
    cur = conn.cursor()
    statement = 'SELECT title, url, published_date, abstract FROM Most_popular'
    cur.execute(statement)
    search_result = []
    for row in cur:
        search_result.append(MostPopular(row))
    return render_template('mostpopular_result.html', result=search_result)



if __name__ == '__main__':
    app.run(debug=True)
