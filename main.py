import requests
import json
import secrets
import sqlite3
import geopy.distance

# nyt_popular_key = secrets.nyt_popular_api_key
nyt_books_key = secrets.nyt_books_api_key
twitter_key = secrets.twitter_api_key
twitter_secret = secrets.twitter_api_secret
twitter_access_token = secrets.twitter_access_token
twitter_access_secret = secrets.twitter_access_secret
google_places_key = secrets.google_places_key
google_key = secrets.google_key
yelp_key = secrets.yelp_api_key
yelp_client_id = secrets.yelp_client_id

#Database
DBNAME = 'data.db'
#cache
CACHE_FNAME = 'cache.json'
def program_start():
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    statement = 'DROP TABLE IF EXISTS \'Books\';'
    cur.execute(statement)
    conn.commit()
    statement = 'DROP TABLE IF EXISTS \'Most_popular\';'
    cur.execute(statement)
    conn.commit()
    statement = 'DROP TABLE IF EXISTS \'Yelp\';'
    cur.execute(statement)
    conn.commit()
    statement = 'DROP TABLE IF EXISTS \'GMap\';'
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE Books (
            'age_group' INTEGER,
            'author' TEXT NOT NULL,
            'created_date' TEXT NOT NULL,
            'description' TEXT NOT NULL,
            'primary_isbn13' TEXT NOT NULL,
            'title' TEXT PRIMARY KEY
        );
    '''

    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE Most_popular (
            'Title' TEXT PRIMARY KEY,
            'url' TEXT NOT NULL,
            'published_date' TEXT NOT NULL,
            'abstract' TEXT NOT NULL
        );
    '''

    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE Yelp (
            'name' TEXT PRIMARY KEY,
            'price' TEXT,
            'address' TEXT,
            'rating' REAL,
            'review_count' INTEGER,
            'url' TEXT,
            'phone' TEXT,
            FOREIGN KEY(name) REFERENCES GMaps(name)
        );'''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE GMap (
            'name' TEXT PRIMARY KEY,
            'address' TEXT,
            'distance' REAL,
            'search_address' TEXT
        );'''
    cur.execute(statement)
    conn.commit()
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

# statement = 'DROP TABLE IF EXISTS \'Books\';'
# cur.execute(statement)
# conn.commit()
# statement = 'DROP TABLE IF EXISTS \'Most_popular\';'
# cur.execute(statement)
# conn.commit()
# statement = 'DROP TABLE IF EXISTS \'Yelp\';'
# cur.execute(statement)
# conn.commit()
# statement = 'DROP TABLE IF EXISTS \'GMap\';'
# cur.execute(statement)
# conn.commit()
#
# statement = '''
#     CREATE TABLE Books (
#         'age_group' INTEGER,
#         'author' TEXT NOT NULL,
#         'created_date' TEXT NOT NULL,
#         'description' TEXT NOT NULL,
#         'primary_isbn13' TEXT NOT NULL,
#         'title' TEXT PRIMARY KEY
#     );
# '''
#
# cur.execute(statement)
# conn.commit()
#
# statement = '''
#     CREATE TABLE Most_popular (
#         'Title' TEXT PRIMARY KEY,
#         'url' TEXT NOT NULL,
#         'published_date' TEXT NOT NULL,
#         'abstract' TEXT NOT NULL
#     );
# '''
#
# cur.execute(statement)
# conn.commit()
#
# statement = '''
#     CREATE TABLE Yelp (
#         'name' TEXT PRIMARY KEY,
#         'price' TEXT,
#         'address' TEXT,
#         'rating' REAL,
#         'review_count' INTEGER,
#         'url' TEXT,
#         'phone' TEXT,
#         FOREIGN KEY(name) REFERENCES GMaps(name)
#     );'''
# cur.execute(statement)
# conn.commit()
#
# statement = '''
#     CREATE TABLE GMap (
#         'name' TEXT PRIMARY KEY,
#         'address' TEXT,
#         'distance' REAL,
#         'search_address' TEXT
#     );'''
# cur.execute(statement)
# conn.commit()


try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)
def make_request_using_cache(baseurl, params):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params)
        # print(resp) #use if getting api error
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        # dumped_json_cache = json.dumps(CACHE_DICTION, sort_keys=True, indent=4, separators=(',', ': '))
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]
#cache request with header
def make_request_using_cache_header(baseurl, params, header):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params=params, headers=header)
        # print(resp) #use if getting api error
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        # dumped_json_cache = json.dumps(CACHE_DICTION, sort_keys=True, indent=4, separators=(',', ': '))
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]






def nyt_book_search(date):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    search_url = 'http://api.nytimes.com/svc/books/v3/lists/overview.json?'

    params = {'published_date': date, 'api-key': nyt_books_key}
    test_search = make_request_using_cache(search_url, params)
    for result in test_search['results']['lists'][1]['books']:
        statement = '''INSERT INTO 'Books' VALUES (?, ?, ?, ?, ?, ?)'''
        insertion = (result['age_group'], result['author'], result['created_date'], result['description'], result['primary_isbn13'], result['title'])
        cur.execute(statement, insertion)
        conn.commit()
def nyt_mostpopular_search(section, time_period):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    search_url = 'http://api.nytimes.com/svc/mostpopular/v2/mostviewed/' + section + '/' + str(time_period) + '.json?'

    params = {'api-key': nyt_books_key}
    test_search = make_request_using_cache(search_url, params)
    # print(test_search)
def map_nearby_search(place):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #calculate latitude longitude of search location
    potential_places = get_place_id(place)
    lat_lon_dict = convert_place_latlong(potential_places)
    lat_lon = str(lat_lon_dict['lat']) + ',' + str(lat_lon_dict['lng'])
    search_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
    #search nearby places on google maps
    params = {'key': google_key, 'location': lat_lon, 'type': 'restaurant', 'rankby': 'distance'}
    google_search = make_request_using_cache(search_url, params)
    for result in google_search['results']:
        # Use latitude to calculate distance of restaurant from search
        lat_lon_pair = (lat_lon_dict['lat'], lat_lon_dict['lng'])
        rest_location = (result['geometry']['location']['lat'], result['geometry']['location']['lng'])
        distance = calculate_distance(lat_lon_pair, rest_location)
        # Insert data into DB
        insert = (result['name'], result['vicinity'], distance, place)
        statement = '''INSERT OR IGNORE INTO GMap VALUES (?, ?, ?, ?)'''
        cur.execute(statement, insert)
        conn.commit()
        yelp_single_search(result['name'], place)
    print(place)
    #and link yelp ratings to result
    # yelp_search(place)
    #maybe create a map on flask to display on website
def yelp_single_search(name, place):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #search yelp for restaurants in a city,

    search_url = 'https://api.yelp.com/v3/businesses/search?'
    params = {'term': name, 'location': place, 'sort_by': 'best_match'}
    header = {'Authorization': 'Bearer %s' % yelp_key,}
    yelp_result = make_request_using_cache_header(search_url, params, header)
    # print(name, place)
    if len(yelp_result['businesses']) == 0:
        statement = '''INSERT OR IGNORE INTO Yelp VALUES (?, ?, ?, ?, ?, ?, ?);'''
        insert = (name, 'null', 'null', 'null', 'null', 'null', 'null')
        cur.execute(statement, insert)
        conn.commit()
        return
    row = yelp_result['businesses'][0]
    address = ''
    for item in row['location']['display_address']:
        address += ' ' + item
    if 'price' not in row:
        row['price'] = ''
    insert = (row['name'], row['price'], address, row['rating'], row['review_count'], row['url'], row['phone'])
    # print(place, row['name'])
    statement = '''INSERT OR IGNORE INTO Yelp VALUES (?, ?, ?, ?, ?, ?, ?);'''
    cur.execute(statement, insert)
    conn.commit()

def get_place_id(place):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    #place autocomplete | Google Places API
    search_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?'
    params = {'input': place, 'key': google_key, 'types': 'address'}
    autocomplete_search = make_request_using_cache(search_url, params)
    # print(autocomplete_search['predictions'])

    #allow user to select between different potential addresses
    # for i in range(len(autocomplete_search['predictions'])):
    #     print(str(1 + i) + ': ' + autocomplete_search['predictions'][i]['description'])
    #     # print('\n\n\n\n')
    # search_index = input('Please select closest address: ')
    # place_id = autocomplete_search['predictions'][int(search_index) - 1]['place_id']

    #add addresses to a list, first being the one to use
    # potential_places = []
    # for item in autocomplete_search['predictions']:
    #     potential_places.append(item)
    # return potential_places
    return autocomplete_search['predictions'][0]

def convert_place_latlong(place):
    place_id = place['place_id']

    #Google Geocode API
    geocode_url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    params = {'place_id': place_id, 'key': google_key}
    geo_search = make_request_using_cache(geocode_url, params)
    lat_lon = geo_search['results'][0]['geometry']['location']

    # print(lat_lon)
    return lat_lon

def calculate_distance(coords_1, coords_2):


    # coords_1 = (52.2296756, 21.0122287)
    # coords_2 = (52.406374, 16.9251681)
    return geopy.distance.vincenty(coords_1, coords_2).miles





#main
# nyt_book_search('2013-05-22')
# nyt_mostpopular_search('Arts', 1)
# convert_place_latlong('ann arbor, MI')
# map_nearby_search('troy, MI')
# yelp_search('troy, MI')
yelp_single_search('Sushi Ya', '4327 Whisper Way Dr.')
