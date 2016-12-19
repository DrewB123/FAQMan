import unittest
from mock import patch
import main
from main import User
import jinja2
from jinja2 import Environment, PackageLoader
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class AddQTests(unittest.TestCase):
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
	def testAddQGet(self, mock):
		# Arrange: Make the web request. 
		addedQuestion = ""
		question_class = ""
		test_request = webapp2.Request.blank('/login')
		# Act: Give the request to the app
		response = test_request.get_response(main.app)
		# Assert: Inspect the response.
		mock.assert_called_with('/home')
	
	# Mocked test: AddQ post() NOQUESTION
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testAddQPostNoQuestion(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		test_request = webapp2.Request.blank('/login', POST={"main.new-question":"", "new-question": "NEW_QUESTION", "main.question": "new-question", "main.question_class": "COMPSCI101", "main.id": "1"})

		# Act: Give the request to the app
		response = test_request.get_response(main.app)
		# Assert: Inspect the response
		mock.assert_called_with('/login')
		self.assertEqual(main.addedQuestion, "")
	
		# Mocked test: AddQ post() HAPPY PATH
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testAddQPostHappyPost(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		test_request = webapp2.Request.blank('/login', POST={"main.new-question": "Q1"})
		#test_question = Questions()
		#test_question.question = 
		# Act: Give the request to the app
		response = test_request.get_response(main.app)
		# Assert: Inspect the response
		mock.assert_called_with('/login')
		self.assertEqual(main.addedQuestion, "")
'''	
	Something we can look into adding in the furture to weed out a question that has already been added - incomplete test
	# Mocked test: AddQ post() DUPLICATE
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testAddQPostDuplicate(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		mock.assert_called_with('/home')
'''
	
	