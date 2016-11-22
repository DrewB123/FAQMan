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

class SuccessHandlerTests(unittest.TestCase):
	# Set up the environment.
	def setUp(self):
		# Create an instance of the Testbed class.
		self.testbed = testbed.Testbed()
		# Activate the testbed, which prepares the service stubs for use.
		self.testbed.activate()
		# Declare test stubs. The first one makes sure that it uses datastore stub.
		self.testbed.init_datastore_v3_stub()
		self.testbed.init_memcache_stub()
		# Clear ndb's in-context cache between tests to prevent data from leaking between tests.
		ndb.get_context().clear_cache()

	# Teardown the environment. 
	def tearDown(self): 
		self.testbed.deactivate()
	
	# Mocked test: ensure that SuccessHandler serves the correct template.
	@patch.object(jinja2.Environment, 'get_template')
	def testSuccessHandler(self, mock): 
		# Arrange.
		request = webapp2.Request.blank('/success')
		# Act. 
		response = request.get_response(main.app)
		# Assert.
		self.assertEqual(main.error, "")
		mock.assert_called_with('success.html')