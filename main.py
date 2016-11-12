#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import urllib
import jinja2
import os
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Questions(ndb.Model):
	question = ndb.StringProperty()
	answer = ndb.StringProperty()
	classQ = ndb.StringProperty()
	answered = ndb.BooleanProperty()
	
	
class User(ndb.Model):
	Fname = ndb.StringProperty()
	Lname = ndb.StringProperty()
	email = ndb.StringProperty()
	password = ndb.StringProperty()
	
	#get list of classes by calling user.classes
	classes = ndb.StringProperty(repeated=True)
	isInstructor = ndb.BooleanProperty()

u = User()
question_class = ""
addedQuestion = ""
error = ""
	
	
class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('home-page.html')
		users = User.query().fetch()		
		self.response.write(template.render({'error':error}))
	
	def post(self):
		template = JINJA_ENVIRONMENT.get_template('home-page.html')
		global error
		login = self.request.get("user_email")
		pw = self.request.get("pass_word")
		user = User.query(User.email == login)
		error=""
		
		if user.count() != 1:
			error = "Invalid Username!"
			self.redirect('/')
			
		else:
			global u
			u = user.get()
			#checks to see if the password is correct
			if u.password == pw:
				#get the number of classes enrolled to use at loop end point in the HTML
				self.redirect('/login')
			else:
				error = "Incorrect password!"
				self.response.write(template.render({'error':error}))	

class SignupHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('signup-page.html')
		self.response.write(template.render({'error':error}))
		
	def post(self):
		global error
		template = JINJA_ENVIRONMENT.get_template('signup-page.html')
		IPASS = "MasterMind"
		isInstructor = False
		
		# check to see if at least one class is selected
		enrolled = False
		for i in range(1, 16):
			cl = "b" + str(i)
			if(self.request.get(cl)):
				enrolled = True
				break
				
		if self.request.get("isInstructor"):
				if self.request.get("isInstructor") == IPASS:
						isInstructor = True
				else:
					# incorrect instructor password entered so reload page with error message
					error = "Not this time student!! If you're an instructor the code you entered is wrong."
					return self.redirect('/signup')
		
		# makes sure the email address is vaild, if not reload the page with error message
		if('@' not in self.request.get("email") or '.' not in self.request.get("email")):
			error = "Please enter a valid email address"
			return self.redirect('/signup')
		
		# verify all necessary data is input to create a user 
		if self.request.get("firstname") and self.request.get("lastname") and self.request.get("email") and enrolled == True:
			users = User.query().fetch()
			dup = False
			
			fname_form = self.request.get("firstname")
			lname_form = self.request.get("lastname")
			email_form = self.request.get("email")
			pw = lname_form + fname_form
			email_form = self.request.get("email")
	
			#checks to see if there is a user with that email address already
			for u in users:
				if u.email == email_form:
					error = "User with that email already exists"
					dup = True		
			if dup == True:
				return self.redirect('/signup')
			
			#if no duplicate is found show a success page and put the user in storage
			else:	
				u = User(Fname=fname_form, Lname=lname_form, email=email_form, password = pw)
				if isInstructor == True:
					u.isInstructor = True
						
				else:
					u.isInstructor = False
		
				for i in range(1, 16):
					cl = "b" + str(i)
					if(self.request.get(cl)):
						u.classes.append(self.request.get(cl))
				u.put()
				return self.redirect('/success')
		
		# Form not filled out fully
		else:
			error = "Please fill in every text box and select at least one class."
			return self.redirect('/signup')
		
		
		
class SuccessHandler(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('success.html')
		self.response.write(template.render())

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		questions = Questions.query().fetch()
		numClasses = len(u.classes)
		if u.isInstructor == True:
			template = JINJA_ENVIRONMENT.get_template('Faculty_landing.html')
			self.response.write(template.render({'user':u, 'classes':numClasses, 'questions':questions, 
							     'added':addedQuestion, 'question_class':question_class}))
			
		else:
			template = JINJA_ENVIRONMENT.get_template('student_landing.html')
			self.response.write(template.render({'user':u, 'classes':numClasses, 'questions':questions,
							     'added':addedQuestion, 'question_class':question_class}))
	
	def post(self):
		global question_class, addedQuestion
		questions = Questions.query().fetch()
		newQ = self.request.get("new-question")
		question_class = self.request.get("add-new-question")
		
		
		if self.request.get("oldpassword") and self.request.get("newpassword") and self.request.get("confirmnewpassword"):
			
			if self.request.get("oldpassword") != u.password:
				addedQuestion = "Incorrect old password input!"
				question_class = ""
				self.redirect('/login')
				
			elif self.request.get("newpassword") == self.request.get("confirmnewpassword"):
				u.password = self.request.get("newpassword")
				u.put()
				addedQuestion = "Your password has been changed!"
				question_class = ""
				self.redirect('/login')
			else:
				addedQuestion = "New passwords don't match "
				question_class = ""
				self.redirect('/login')
		
		elif self.request.get("new-question"):
			Q = Questions(question = newQ, classQ = question_class, answered = False)
			Q.put()
			addedQuestion = "You're question has been added to the list of questions for "
			self.redirect('/login')
			
		else:
			addedQuestion = "You have to ask a question for someone to be able to answer it!"
			question_class = ""
			self.redirect('/login')

			
class ClearHandler(webapp2.RequestHandler):
	def get(self):
		#deleting all users
		users = User.query()
		for u in users:
			u.key.delete()
		
		#deleting all questions		
		questions = Questions.query()
		for q in questions:
			q.key.delete()
		self.redirect('/signup')
		
app = webapp2.WSGIApplication([
    ('/', MainHandler),
	('/signup', SignupHandler),
	('/success', SuccessHandler),
	('/login', LoginHandler),
	('/clear', ClearHandler)
], debug=True)
