import unittest
from mock import patch
import main
from main import User
import jinja2
from jinja2 import Environment, PackageLoader
import webapp2
from google.appengine.ext import ndb
from google.appengine.ext import testbed

class SignupHandlerTests(unittest.TestCase):
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

	# Mocked test: ensure that the SignUpHandler get() delivers the correct html page. 
	@patch.object(jinja2.Environment, 'get_template')
	def testSignUpHandlerGet(self, mock):
		# Arrange: Make the web request. 
		test_request = webapp2.Request.blank('/signup')
		# Act: Give the request to the app. 
		response = test_request.get_response(main.app)
		# Assert: Inspect the response.
		mock.assert_called_with('signup-page.html')

	# Mocked test: ensure that the SignUpHandler post() does not allow Student 
	# to register as an Instructor. 
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testSignUpHandlerBADSTUDENTPost(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		test_request = webapp2.Request.blank('/signup', POST={"firstname" : "TESTFIRST", "lastname" : "TESTLAST", "email" : "fake_user@email.com", "password" : "PASSWORD", "b9" : "COMPSCI101"})
		main.isInstructor = False
		test_request.method = 'POST'
		mock.return_value = None

		# Act
		response = test_request.get_response(main.app)

		# Assert: Inspect the response
		self.assertEqual(main.error, "Not this time student!! If you're an instructor the code you entered is wrong.")
		mock.assert_called_with('/signup')
	
	# Mocked test: ensure that the SignUpHandler post() does not allow duplicate users.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testSignUpHandlerBADSTUDENTPost(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		test_user = User()
		test_user.email = "fake_user@email.com"
		test_user.password = "PASSWORD"
		test_user.put()

		test_request = webapp2.Request.blank('/signup', POST={"firstname" : "TESTFIRST", "lastname" : "TESTLAST", "email" : "fake_user@email.com", "password" : "PASSWORD", "b9" : "COMPSCI101"})
		main.isInstructor = False
		test_request.method = 'POST'
		mock.return_value = None

		# Act
		response = test_request.get_response(main.app)

		# Assert: Inspect the response
		self.assertEqual(main.error, "User with that email already exists")
		mock.assert_called_with('/signup')
	
	# Mocked test: ensure that the SignUpHandler post() does not allow a user to sign up with an
	# improperly-formatted email address. 
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testSignUpHandlerBADEMAILPost(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		test_request = webapp2.Request.blank('/signup', POST={"firstname" : "TESTFIRST", "lastname" : "TESTLAST", "email" : "fake_useremail.com", "password" : "PASSWORD", "b9" : "COMPSCI101"})
		test_request.method = 'POST'
		mock.return_value = None

		# Act
		response = test_request.get_response(main.app)

		# Assert: Inspect the response
		self.assertEqual(main.error, "Please enter a valid email address")
		mock.assert_called_with('/signup')

	# Mocked test: ensure that the SignUpHandler post() requires at least one course to be checked before registration.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testSignUpHandlerNOCLASSPost(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		test_request = webapp2.Request.blank('/signup', POST={"firstname" : "TESTFIRST", "lastname" : "TESTLAST", "email" : "fake_useremail@.com", "password" : "PASSWORD"})
		test_request.method = 'POST'
		mock.return_value = None

		# Act
		response = test_request.get_response(main.app)

		# Assert: Inspect the response
		self.assertEqual(main.error, "Please fill in every text box and select at least one class.")
		mock.assert_called_with('/signup')
	
	# Mocked test: ensure that the SignUpHandler post() requires a name for registration.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testSignUpHandlerNONAMEPost(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		test_request = webapp2.Request.blank('/signup', POST={"firstname" : "", "lastname" : "TESTLAST", "email" : "fake_useremail@.com", "password" : "", "b9" : "COMPSCI101"})
		test_request.method = 'POST'
		mock.return_value = None

		# Act
		response = test_request.get_response(main.app)

		# Assert: Inspect the response
		self.assertEqual(main.error, "Please fill in every text box and select at least one class.")
		mock.assert_called_with('/signup')

	# Mocked test: ensure that the SignUpHandler post() works as expected under 'error-free' conditions.
	@patch.object(webapp2.RequestHandler, 'redirect')
	def testSignUpHandlerHappyPost(self, mock): 
		# Arrange: Make the web request with all of the necessary information.
		test_request = webapp2.Request.blank('/signup', POST={"firstname" : "TESTFIRST", "lastname" : "TESTLAST", "email" : "fake_user@email.com", "password" : "PASSWORD", "b9" : "COMPSCI101"})
		test_request.method = 'POST'
		mock.return_value = None

		# Act
		response = test_request.get_response(main.app)

		# Assert: Inspect the response
		self.assertEqual(main.error, "")
		mock.assert_called_with('/success')

	# Teardown the environment. 
	def tearDown(self): 
		self.testbed.deactivate()