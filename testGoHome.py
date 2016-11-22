import unittest
from mock import patch
import main
from main import User
import jinja2
from jinja2 import Environment, PackageLoader
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class GoHomeTests(unittest.TestCase):
	# Set up the environment.
	def setUp(self):
		# Create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Declare test stubs. The first one makes sure that it uses the fake datastore.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		# Clear ndb's in-context cache between tests to prevent data from leaking between tests.
		ndb.get_context().clear_cache()
	
	# Set up the environment.
	def setUp(self):
		# Create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Declare test stubs. The first one makes sure that it uses the fake datastore.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		# Clear ndb's in-context cache between tests to prevent data from leaking between tests.
		ndb.get_context().clear_cache()

	# Teardown the environment. 
	def tearDown(self): 
		self.testbed.deactivate()
	
	# Mocked test: ensure that in get(), the cookie is deleted and that no errors occured.
	# Two patch objects can be passed. The second will check out the cookies.
	@patch.object(webapp2.RequestHandler, 'redirect')
	@patch.object(webapp2.Response, 'delete_cookie')
	def testGoHomeGet(self, mock_del_cookie, mock_redir): 
		# Arrange: Make request to get().
		request = webapp2.Request.blank('/goHome')
		# This adds a cookie called uname. 
		request.cookies['uname'] = 'TESTUSER@email.com'

		# Act: Give the request to the app. 
		response = request.get_response(main.app)
		
		# Assert: global variables are empty
		#mock_del_cookie.assert_called_once()
		mock_del_cookie.assert_called_with('uname')
		self.assertEqual(main.error, "")
		mock_redir.assert_called_with('/home')
		
	@patch.object(webapp2.RequestHandler, 'redirect')
	@patch.object(webapp2.Response, 'delete_cookie')
	def testGoHomeGet(self, mock_del_cookie, mock_redir): 
		# Arrange: Make request to get().
		request = webapp2.Request.blank('/goHome')
		# This adds a cookie called uname. 
		request.cookies['uname'] = 'TESTUSER@email.com'

		# Act: Give the request to the app. 
		response = request.get_response(main.app)
		request.method = 'POST'
		
		# Assert: global variables are empty
		#mock_del_cookie.assert_called_once()
		mock_del_cookie.assert_called_with('uname')
		self.assertEqual(main.error, "")
		mock_redir.assert_called_with('/home')

	# Teardown the environment. 
	def tearDown(self): 
		self.testbed.deactivate()