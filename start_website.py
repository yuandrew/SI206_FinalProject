from flask import Flask, render_template, request, redirect


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/select', methods = ['POST'])
def signup():
    location = request.form['location']
    search_type = request.form['search_type']
    return redirect('/' + search_type)
#TODO: not sure how to redirect to different page based off of form selection
# @app.route('/', methods = ['GET'])
# def result():
#     result = request.form
@app.route('/restaurantsearch')
def restaurant_search():
    return render_template('restaurant.html')

@app.route('/bestsellers')
def best_sellers():
    return render_template('bestsellers.html')

@app.route('/mostpopular')
def most_popular():
    return render_template('mostpopular.html')

@app.route('/nearbysearch')
def nearby_search():
    return render_template('nearbysearch.html')





if __name__ == '__main__':
    app.run(debug=True)
