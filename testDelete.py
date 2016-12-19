import unittest
from mock import patch
import main
from main import User
import jinja2
from jinja2 import Environment, PackageLoader
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class DeleteTests(unittest.TestCase):
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
		
	# Mocked test: Delete get()
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testDeleteGet(self, mock):
		# Arrange: Make the web request. 
		test_request = webapp2.Request.blank('/FAQ')
		# Act: Give the request to the app
		response = test_request.get_response(main.app)
		# Assert: Inspect the response.
		mock.assert_called_with('/home')	

	# Mocked test: Delete post()
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testDeletePostRedirect(self, mock):
		# Arrange: Make the web request. 
		test_request = webapp2.Request.blank('/FAQ', POST={"Questions.inFAQ": True})
		# Act: Give the request to the app
		response = test_request.get_response(main.app)
		# Assert: Inspect the response.
		mock.assert_called_with('/FAQ')	
		
'''
	# Mocked test: Delete post() QUESTION NOT IN FAQ - this is something we can add in for the future
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testDeleteNOTINFAQPost(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		test_request = webapp2.Request.blank('/FAQ', POST={"Questions.inFAQ": False, "Questions.classQ": main.question_class})
		test_request.method = 'POST'
		mock.return_value = None
		
		# Act
		response = test_request.get_response(main.app)

		# Assert: Inspect the response
		self.assertEqual(main.error, "The question you are trying to remove is not in the FAQ.")
		mock.assert_called_with('/home')
'''












		