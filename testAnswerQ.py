import unittest
from mock import patch
import main
from main import User
import jinja2
from jinja2 import Environment, PackageLoader
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class AnswerQTests(unittest.TestCase):
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
		
	# Mocked test: AnswerQ get()
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testAnswerQGet(self, mock):
		# Arrange: Make the web request. 
		test_request = webapp2.Request.blank('/login')
		# Act: Give the request to the app. 
		response = test_request.get_response(main.app)
		# Assert: Inspect the response.
		mock.assert_called_with('/home')
		
		# Mocked test: Answer post() Back to FAQ page
		
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testAnswerQPost(self, mock): 
		# Arrange: Make the web request. 
		test_request = webapp2.Request.blank('/login', POST={"firstname" : "TESTFIRST", "lastname" : "TESTLAST", "email" : "fake_useremail@.com", "password" : "PASSWORD"})
		test_request.method = 'POST'
		mock.return_value = None
		
		# Act: Give the request to the app. 
		response = test_request.get_response(main.app)
		# Assert: Inspect the response.
		mock.assert_called_with('/login')	
		
	# Teardown the environment. 
	def tearDown(self): 
		self.testbed.deactivate()