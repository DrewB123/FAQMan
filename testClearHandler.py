import unittest
from mock import patch
import main
from main import User
import jinja2
from jinja2 import Environment, PackageLoader
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class ClearHandlerTests(unittest.TestCase):
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
		
	# Mocked test: ClearHandler get()
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testClearHandlerGet(self, mock):
		# Arrange: Make the web request with all of the necessary information.
		test_request = webapp2.Request.blank('/signup', POST={"firstname" : "TESTFIRST", "lastname" : "TESTLAST", "email" : "fake_useremail@.com", "password" : "PASSWORD"})
		test_request.method = 'POST'
		mock.return_value = None
		
		# Arrange: Make the web request.
		request = webapp2.Request.blank('/signup')
		
		# Act
		response = test_request.get_response(main.app)
		
		# Assert: Inspect the response
		mock.assert_called_with('/signup')
		
	# Teardown the environment. 
	def tearDown(self): 
		self.testbed.deactivate()		
		