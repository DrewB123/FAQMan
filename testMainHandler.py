import unittest
from mock import patch
import mock
import urllib
import os
import main
from main import User
import jinja2
from jinja2 import Environment, PackageLoader
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import testbed

#app = TestApp(main.app)

class MainHandlerTests(unittest.TestCase):
	# Set up the environment.
	def setUp(self):
		# Create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Declare test stubs. The first one makes sure that it uses the fake datastore.
		# The second one...I don't actually know what it does, but it was in the documentation.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		# Clear ndb's in-context cache between tests to prevent data from leaking between tests.
		# Alternatively: ndb.get_context().set_cache_policy(False)
		ndb.get_context().clear_cache()

	# Teardown the environment. 
	def tearDown(self): 
		self.testbed.deactivate()
	
	### START TESTS ###

	# Unmocked test
	# Test MainHandler get() delivers the correct html pages. 
	def testMainHandlerget(self): 
		# Make a fake web request using the path to simulate user. 
		request = webapp2.Request.blank('/')
		# Retrieve the response. This simulates what would happen if a user 
		# tried to access the homepage. 
		response = request.get_response(main.app)

		# Check to see if the status codes are the same (i.e., that the request succeeded)
		# and served the page. 
		self.assertEqual(response.status_int, 200)
		
		# Check to see if the html for home-page was rendered.
		isTitleCorrect = False
		isFAQCorrect = False

		if "<title>FAQMan: Home Page</title>" in response.body:
			isTitleCorrect = True
		self.assertTrue(isTitleCorrect)

		if 'h3 id="faq-lab">FAQ LISTINGS</h3>' in response.body: 
			isFAQCorrect = True
		self.assertTrue(isFAQCorrect)
	
	# Mocked test; verify that the correct template is served. 
	# patch() will confirm whether or not a function is called.
	# It will determine what the *real* function is called with.
	# Here, the first param of patch() is the name of the object that
	# is being overwritten. The second is the name of the function to keep 
	# track of. It's like spying. The "fake" one pretends to be the original, 
	# and gathers information about it.
	@patch.object(jinja2.Environment, 'get_template')
	# The patched function is called 'mock' in this context.
	def testMainHandlerGetMocked(self, mock): 
		# Arrange: Make a fake web request that will be routed to MainHandler's get().
		request = webapp2.Request.blank('/')
		# Act: Give the request to the app. 
		response = request.get_response(main.app)
		# Assert
		mock.assert_called_with('home-page.html')
		# steve holt
	
	# Mocked test: verify that the post() redirect works when an error happens.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testMainHandlerPostEmailError(self, mock): 
		# Arrange: If there's not exactly one user, an error occurs. 
		# POST is a dictionary; it adds this data to a request object...or something. I think this is unnecessary.
		test_request = webapp2.Request.blank('/', POST={"user_email": "fake_user@email.com", "pass_word" : "FAKEPASSWORD"})
		test_request.method = 'POST'
		# I have no idea why this line is necessary. 
		mock.return_value = None
		# Act: Give the request to the app. 
		response = test_request.get_response(main.app)

		# Assert: Inspect the response
		mock.assert_called_with('/')
		self.assertEqual(main.error, "Invalid email!")
	
	# Mocked test: Test the "incorrect password" error handling.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testMainHandlerPostPWError(self, mock): 
		# Arrange: Put a User in the datastore stub; POST the wrong password.
		test_User = User()
		test_User.email = "fake_user@email.com"
		test_User.password = "PASSWORD"
		test_User.put()
		test_request = webapp2.Request.blank('/', POST={"user_email" : "fake_user@email.com", "pass_word" : "WRONGPASSWORD"})
		test_request.method = 'POST'
		mock.return_value = None

		# Act: Give the request to the app.
		response = test_request.get_response(main.app)

		# Assert: Inspect the response. 
		mock.assert_called_with('/')
		self.assertEqual(main.error, "Incorrect password!")
	
	# Mocked test: Login
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testMainHandlerPostLogin(self, mock): 
		# Arrange: Put a User in the datastore stub; POST the correct password. 
		test_User = User()
		test_User.email = "fake_user@email.com"
		test_User.password = "PASSWORD"
		test_User.put()
		test_request = webapp2.Request.blank('/', POST={"user_email" : "fake_user@email.com", "pass_word" : "PASSWORD"})
		test_request.method = 'POST'
		mock.return_value = None

		# Act: Give the request to the app.
		response = test_request.get_response(main.app)

		# Assert: Inspect the response. 
		# The "error" should be blank. 
		mock.assert_called_with('/login')
		self.assertEqual(main.error, "")










# This has something to do with the way the unittest works; 
# this causes the program to run...less like a script. 
if __name__ == '__main__':
	unittest.main()