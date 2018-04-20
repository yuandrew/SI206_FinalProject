import unittest
from main import *

program_start()


class TestDatabase(unittest.TestCase):
    def test_book_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        nyt_book_search('2016-01-01')
        sql = 'SELECT Title FROM Books'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertNotEqual(len(result_list), 0)
        self.assertIn(('BETWEEN THE WORLD AND ME',), result_list)
    def test_popular_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        nyt_mostpopular_search('Arts', 1)
        sql = 'SELECT Title FROM Most_popular'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertNotEqual(len(result_list), 0)
        self.assertIn(('Colbert Revels in News of a Connection Between Hannity and Cohen',), result_list)

    def test_gmap_yelp_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
        map_nearby_search('530 S State St, Ann Arbor, MI')
        sql = 'SELECT name FROM Yelp'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertNotEqual(len(result_list), 0)
        self.assertIn(('Pita Kabob Grill',), result_list)

        sql = 'SELECT name FROM GMap'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertNotEqual(len(result_list), 0)
        self.assertIn(('Asian Legend',), result_list)

class TestUtility(unittest.TestCase):
    def test_latlon(self):
        place_id = get_place_id('530 S State St, Ann Arbor, MI, USA')
        self.assertEqual('ChIJm6MvgkeuPIgRrQI6vPMnchY', place_id)
        place_id = get_place_id('1324 Lafayette Ave, Kalamazoo, MI, USA')
        self.assertEqual('ChIJg-cKLLZ3F4gRwOGhtTKLoO8', place_id)
    def test_distance(self):
        coord_1 = (38.8977, 77.0365)
        coord_2 = (40.6892, 74.0445)
        coord_3 = (38.8899, 77.0091)
        self.assertEqual(201.55398822430246, calculate_distance(coord_1, coord_2))
        self.assertEqual(201.55398822430232, calculate_distance(coord_2, coord_1))
        self.assertEqual(200.7435548093539, calculate_distance(coord_2, coord_3))
    def test_placeid(self):
        place_id = 'ChIJ37HL3ry3t4kRv3YLbdhpWXE'
        lat_lon = convert_place_latlong(place_id)
        self.assertEqual(lat_lon['lat'], 38.8976763)
        self.assertEqual(lat_lon['lng'], -77.0365298)
unittest.main()
