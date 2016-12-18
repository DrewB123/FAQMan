import unittest
from mock import patch
import main
from main import User
import jinja2
from jinja2 import Environment, PackageLoader
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class StartupHandlerTests(unittest.TestCase):
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
	
	# Mocked test: ensure that get() initializes Qcount and redirects to the home page.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testStartUpHandlerGet(self, mock): 
		# Arrange: Make request to get().
		request = webapp2.Request.blank('/')
		# Act: Give the request to the app. 
		response = request.get_response(main.app)
		# Assert: global variables are empty
		mock.assert_called_with('/home')
		
	# Mocked test: ensure that '/' redirects to the home page.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testStartupHandlerPost(self, mock): 
		# Arrange: Make request to get().
		request = webapp2.Request.blank('/')
		# Act: Give the request to the app. 
		response = request.get_response(main.app)
		# Assert: global variables are empty
		mock.assert_called_with('/home')

	# Teardown the environment. 
	def tearDown(self): 
		self.testbed.deactivate()