from flask import Flask, render_template, request, redirect
import main
import sqlite3
import requests

app = Flask(__name__)
pub_location = ''
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
@app.route('/')
def home():
    main.program_start()
    return render_template('home.html')


@app.route('/select', methods=['POST'])
def signup():
    # location = request.form['location']
    search_type = request.form['search_type']
    return redirect('/' + search_type)

@app.route('/restaurantsearch')
def restaurant_search():
    return render_template('restaurant.html')

@app.route('/restaurantsearch/confirm', methods=['POST'])
def restaurant_search_confirm():
    search_type = request.form['search_type']
    location = request.form['location']

    if search_type == 'nearby':
        # potential_places = main.map_nearby_search(location)
        main.map_nearby_search(location)
        pub_location = location
        return redirect('/restaurantsearch/nearby')
    main.yelp_search(location)
    return redirect('/restaurantsearch/city')

@app.route('/restaurantsearch/nearby')
def restaurant_search_nearby():
    conn = sqlite3.connect(main.DBNAME)
    cur = conn.cursor()
    statement = '''SELECT search_address FROM Gmap'''
    cur.execute(statement)
    search = ''
    for row in cur:
        if search == '':
            search = row[0]
    statement = 'SELECT GMap.name, GMap.address, distance, price, rating, review_count, url, phone FROM Gmap JOIN Yelp ON Yelp.name=GMap.name'# WHERE GMap.search_address=\'' + pub_location + '\''
    cur.execute(statement)
    search_result = []
    for row in cur:
        search_result.append(Nearby(row))
    return render_template('restaurant_nearby.html', result=search_result, place=search)

@app.route('/restaurantsearch/city')
def restaurant_search_city():
    statement = ''' '''
    return render_template('restaurant_city.html')



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
    statement = ''' '''
    return render_template('bestsellers_result.html')



@app.route('/mostpopular')
def most_popular():
    return render_template('mostpopular.html')

@app.route('/nearbysearch')
def nearby_search():
    return render_template('nearbysearch.html')





if __name__ == '__main__':
    app.run(debug=True)
