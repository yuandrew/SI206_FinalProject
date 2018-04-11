import requests
import json
import secrets

# nyt_popular_key = secrets.nyt_popular_api_key
nyt_books_key = secrets.nyt_books_api_key
twitter_key = secrets.twitter_api_key
twitter_secret = secrets.twitter_api_secret
twitter_access_token = secrets.twitter_access_token
twitter_access_secret = secrets.twitter_access_secret
google_places_key = secrets.google_places_key

CACHE_FNAME = 'cache.json'
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
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION)
        # dumped_json_cache = json.dumps(CACHE_DICTION, sort_keys=True, indent=4, separators=(',', ': '))
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

def nyt_book_search(date):
    search_url = 'http://api.nytimes.com/svc/books/v3/lists/overview.json?'

    params = {'published_date': date, 'api-key': nyt_books_key}
    test_search = make_request_using_cache(search_url, params)
    print(test_search)

def nyt_mostpopular_search(section, time_period):
    search_url = 'http://api.nytimes.com/svc/mostpopular/v2/mostviewed/' + section + '/' + str(time_period) + '.json?'

    params = {'api-key': nyt_books_key}
    test_search = make_request_using_cache(search_url, params)
    print(test_search)
#main
# nyt_book_search('2013-05-22')
nyt_mostpopular_search('Arts', 1)
