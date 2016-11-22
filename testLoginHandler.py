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

class LoginHandlerTests(unittest.TestCase):
	# Set up the environment.
	def setUp(self):
		# Create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Declare test stubs. The first one makes sure that it uses the datastore stub.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		# Clear ndb's in-context cache between tests to prevent data from leaking between tests.
		ndb.get_context().clear_cache()

	# Teardown the environment. 
	def tearDown(self): 
		self.testbed.deactivate()
	
	# Mocked test
	@patch.object(jinja2.Environment, 'get_template')
	# The patched function is called 'mock' in this context.
	def testMainHandlerGetMocked(self, mock): 
		# Arrange: Make a fake web request that will be routed to MainHandler's get().
		request = webapp2.Request.blank('/home')
		# Act: Give the request to the app. 
		response = request.get_response(main.app)
		# Assert
		mock.assert_called_with('home-page.html')
		# steve holt
	
	# Mocked test: verify that the post() redirect works when a duplicate user error happens.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testMainHandlerPostEmailError(self, mock): 
		# Arrange: If there's not exactly one user, an error occurs. 
		# POST is a dictionary; it adds this data to a request object...or something. I think this is unnecessary.
		test_request = webapp2.Request.blank('/home', POST={"user_email": "fake_user@email.com", "pass_word" : "FAKEPASSWORD"})
		test_request.method = 'POST'
		# I have no idea why this line is necessary. 
		mock.return_value = None
		# Act: Give the request to the app. 
		response = test_request.get_response(main.app)

		# Assert: Inspect the response
		mock.assert_called_with('/home')
		self.assertEqual(main.error, "Invalid email!")
	
	# Mocked test: ensure that the application does not allow login with an incorrect password.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testMainHandlerPostPWError(self, mock): 
		# Arrange: Put a User in the datastore stub; POST the wrong password.
		test_User = User()
		test_User.email = "fake_user@email.com"
		test_User.password = "PASSWORD"
		test_User.put()
		test_request = webapp2.Request.blank('/home', POST={"user_email" : "fake_user@email.com", "pass_word" : "WRONGPASSWORD"})
		test_request.method = 'POST'
		mock.return_value = None

		# Act: Give the request to the app.
		response = test_request.get_response(main.app)

		# Assert: Inspect the response. 
		mock.assert_called_with('/home')
		self.assertEqual(main.error, "Incorrect password!")
	
	# Mocked test: ensure that login occurs when the correct user name and password are entered.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testMainHandlerPostLogin(self, mock): 
		# Arrange: Put a User in the datastore stub; POST the correct password. 
		test_User = User()
		test_User.email = "fake_user@email.com"
		test_User.password = "PASSWORD"
		test_User.put()
		test_request = webapp2.Request.blank('/home', POST={"user_email" : "fake_user@email.com", "pass_word" : "PASSWORD"})
		test_request.method = 'POST'
		mock.return_value = None

		# Act: Give the request to the app.
		response = test_request.get_response(main.app)

		# Assert: Inspect the response. 
		# The "error" should be blank. 
		mock.assert_called_with('/login')
		self.assertEqual(main.error, "")

	@patch.object(webapp2.RequestHandler, 'redirect')
	@patch.object(webapp2.Response, 'set_cookie')
	def testMainHandlerCookie(self, mock_set_cookie, mock_redir):
		user = User()
		user.Fname = "Matt"
		user.Lname = "K"
		user.email = "mattk@uwm.edu"
		user.password = "KMatt"
		user.put()
		request = webapp2.Request.blank('/home', POST={"user_email": "mattk@uwm.edu", "pass_word" : "KMatt"})
		request.method = 'POST'
		mock_redir.return_value = None
		
		response = request.get_response(main.app)
		
		mock_set_cookie.assert_called_with('uname', user.email, path='/')
		self.assertEqual(main.error, "")
		mock_redir.assert_called_with('/login')

# 'main' method. 
if __name__ == '__main__':
	unittest.main()