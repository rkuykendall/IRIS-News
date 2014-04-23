import unittest
from sqlalchemy import *
import os

# Set enviornment before importing any database classes
os.environ["CONFIG_PATH"] = "database.TestingConfig"
from feed import *
from database import Base, engine, session, app
 
class TestFeed(unittest.TestCase):
    def setUp(self):

        print "# # # # # # # # # # # # # # # # # # # #"
        print "   "+str(app.config['NAME'])
        print "# # # # # # # # # # # # # # # # # # # #"
        
        # Set up the tables in the database
        Base.metadata.create_all(engine)        

    def test_db(self):
        feed = Feed('data/2014-04-05_16-54.atom')        
        feed.save(engine)
        feed2 = Feed()
        feed2.load(engine)
        self.assertEqual(len(feed.articles),89)
        self.assertEqual(len(feed2.articles),89)
    
    def test_from_feed(self):
        # # Commented out because search doesn't always have 10 things to return
    	# q="flight"
    	# url="http://api.feedzilla.com/v1/categories/27/articles/search.atom?q="+q+"&count=10"
    	url = "http://api.feedzilla.com/v1/categories/16/articles.atom?count=10"
        feed = Feed(url)
        self.assertEqual(len(feed.articles),10)        

    def test_from_file(self):
        feed = Feed('data/2014-04-05_16-54.atom')
        self.assertEqual(len(feed.articles),89)
        
    def test_duplicate_articles(self):
        feed = Feed('data/2014-04-05_16-54.atom')
        feed.add_feed('data/2014-04-05_16-54.atom')
        self.assertEqual(len(feed.articles),89)

    def test_cray(self):
    	url = "http://api.feedzilla.com/v1/categories/16/articles.atom?count=10"
        feed = Feed('data/2014-04-05_16-54.atom')
        feed.add_feed(url)
        self.assertEqual(len(feed.articles),99)

    def test_cray2(self):
    	url = "http://api.feedzilla.com/v1/categories/16/articles.atom?count=20"
        feed = Feed('data/2014-04-05_16-54.atom')
        feed.add_feed(url)
        feed.add_feed(url)
        self.assertEqual(len(feed.articles),109)

