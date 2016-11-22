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
	
	# Mocked test: ensure that cookies function on login for Student user.
	@patch.object(jinja2.Environment, 'get_template') 
	def testLoginHandlerCookieStudent(self, mock):
		user = User()
		user.Fname = "Matt"
		user.Lname = "K"
		user.email = "mattk@uwm.edu"
		user.password = "KMatt"
		user.isInstructor = False
		main.u = user
		user.put()
		request = webapp2.Request.blank('/login')
		request.cookies['uname'] = "mattk@uwm.edu"
		response = request.get_response(main.app)
		mock.assert_called_with('student_landing.html')

	# Mocked test: ensure that cookies function on login for Faculty
	@patch.object(jinja2.Environment, 'get_template') 
	def testLoginHandlerCookieFaculty(self, mock):
		user = User()
		user.Fname = "Matt"
		user.Lname = "K"
		user.email = "mattk@uwm.edu"
		user.password = "KMatt"
		user.isInstructor = True
		main.u = user
		user.put()
		request = webapp2.Request.blank('/login')
		request.cookies['uname'] = "mattk@uwm.edu"
		response = request.get_response(main.app)
		mock.assert_called_with('Faculty_landing.html')