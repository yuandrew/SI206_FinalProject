# SI206_FinalProject

[Link to project specifications](https://docs.google.com/document/d/19vyyYe2d-VGWf_sN3y82lbJaitR4eN-LitTRz2COu1Q/edit)

Data sources used:  
&nbsp;&nbsp;&nbsp;&nbsp;[Yelp Fusion Business Search](https://www.yelp.com/developers/documentation/v3/business_search)  
&nbsp;&nbsp;&nbsp;&nbsp;[New York Times Books API](https://developer.nytimes.com/books_api.json)  
&nbsp;&nbsp;&nbsp;&nbsp;[New York Times Most Popular API](https://developer.nytimes.com/most_popular_api_v2.json)  
&nbsp;&nbsp;&nbsp;&nbsp;[Google Places API Web Service](https://developers.google.com/places/web-service/search)  
&nbsp;&nbsp;&nbsp;&nbsp;[Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/intro)  

Keys needed:  
&nbsp;&nbsp;&nbsp;&nbsp;Google API Key  
&nbsp;&nbsp;&nbsp;&nbsp;New York Times API Key  
&nbsp;&nbsp;&nbsp;&nbsp;Yelp Client ID and API Key  

See sample_secret.py for formatting and how to implement.



Brief Overview: The most important functions in my code are in main.py, which contain all of the API call functions. Each function calls the API in its name. As for start_website.py, that is used for Flask to create the website based off of templates. There are classes used when SELECTing data from the database to insert into the webpages. There is also a large list of most_popular_items as a category bank for easy selection when calling the Most Popular command.

To run the program, activate your virtual environment. Then run 'pip install -r requirements.txt' to correctly set up the virtual environment. Finally, run 'python start_website.py'. main.py is called from start_website.py when needed, so there is no need to explicitly call main.py.
