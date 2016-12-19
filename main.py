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
import time
from google.appengine.ext import ndb
from datetime import datetime 
from google.appengine.api.mail import EmailMessage
from google.appengine.api.mail_errors import MissingRecipientsError
from google.appengine.api import app_identity
from jinja2 import Environment, FileSystemLoader

JINJA_ENVIRONMENT = jinja2.Environment(loader = jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Questions(ndb.Model):
	question = ndb.StringProperty()
	answer = ndb.StringProperty()
	classQ = ndb.StringProperty()
	inFAQ = ndb.BooleanProperty()
	id = ndb.IntegerProperty()
	asker = ndb.StringProperty()
	
	timestamp = ndb.DateTimeProperty(auto_now = True)
	timestampanswered = ndb.DateTimeProperty(auto_now = True)
	
class Course(ndb.Model):
	classlist = ndb.StringProperty(repeated=True)
	name = ndb.StringProperty()
	subject = ndb.StringProperty()
	id = ndb.IntegerProperty()

class User(ndb.Model):
	Fname = ndb.StringProperty()
	Lname = ndb.StringProperty()
	email = ndb.StringProperty()
	password = ndb.StringProperty()
	isInstructor = ndb.BooleanProperty()
	
	#get list of classes by calling user.classes
	classes = ndb.StringProperty(repeated=True)

# ##############################
# Email setup
JE = Environment(loader=FileSystemLoader('.'))
email_message = EmailMessage()

def redirect_to_main(response, message, duration):
    response.write(message)
    response.write('<meta http-equiv="refresh" content="' + str(duration) + ';url=/" />')
	
class Email(ndb.Model):
	from_address = ndb.StringProperty()
	to_addresses = ndb.StringProperty(repeated=True)
	subject      = ndb.StringProperty()
	body         = ndb.StringProperty()
	sent_date    = ndb.DateTimeProperty(auto_now=True)

	@staticmethod
	def get_email_from(urlsafe_key):
		return ndb.Key(urlsafe=urlsafe_key).get()

	@staticmethod
	def store_email_from(email_message):
		Email(
			from_address = email_message.sender,
			to_addresses = email_message.to,
			subject      = email_message.subject,
			body         = email_message.body
		).put()

		
	@staticmethod
	def send_email(sender, to, subject, message):
		email_message.sender  = sender
		email_message.to      = to
		email_message.subject = subject
		email_message.body    = message
		email_message.check_initialized()
		email_message.send()

		Email.store_email_from(email_message)

	def __str__(self):
		return '%30s | %30s | %30s | %30s | %s' % (
			self.from_address,
			self.to_addresses,
			self.sent_date,
			self.subject,
			self.body
		)
		
question_class = ""
addedQuestion = ""
error = ""
classClicked = ""
#This is prone to error and stale data.
#If you need to have the number of questions or anything
#in the code, you should ALWAYS query for it, not save
#the value in this variable
#Qcount = 0
#Ccount = 0




# On startup get a count of all questions to set Qcount
# and go to the home page.
class StartupHandler(webapp2.RequestHandler):
	def get(self):
		if self.request.cookies.get('uname'):
			self.response.delete_cookie('uname')
		self.redirect('/home')
	
	def post(self):
		self.redirect('/home')
		
# ##############################################################################################################################################		
class MainHandler(webapp2.RequestHandler):
	
	def get(self):
		global question_class, addedQuestion, error
		question_class = ""
		addedQuestion = ""
		template = JINJA_ENVIRONMENT.get_template('home-page.html')	
		self.response.write(template.render({'error':error}))
	
	def post(self):
		template = JINJA_ENVIRONMENT.get_template('home-page.html')
		global error
		login = self.request.get("user_email")
		pw = self.request.get("pass_word")

# ##############CHECK FOR ADMIN###############################################################################################################
		if login == "admin":
			if pw == "BATMAN":
				self.response.set_cookie('uname', login, path='/')
				return self.redirect('/admin')
# #############################################################################################################################################
		else:
			user = User.query(User.email == login)
			
			if user.count() != 1:
				error = "Invalid email!"
				return self.redirect('/home')
			
			else:
				u = User()
				u = user.get()
				#checks to see if the password is correct
				if u.password == pw:
					error = ""
					self.response.set_cookie('uname', u.email, path='/')
					return self.redirect('/login')
				else:
					error = "Incorrect password!"
					return self.redirect('/home')

# ##############################################################################################################################################		
class SignupHandler(webapp2.RequestHandler):
	def get(self):
		courses = Course.query().fetch()
		subjects = []

		for course in courses:
			if course.subject not in subjects:
				subjects.append(course.subject)

		template = JINJA_ENVIRONMENT.get_template('signup-page.html')
		self.response.write(template.render({'subjects': subjects, 'courses': courses}))
		
	def post(self):
		global error
		template = JINJA_ENVIRONMENT.get_template('signup-page.html')
		
#   ########PASSWORD TO MAKE AN INSTRUCTOR USER####################
		IPASS = "MasterMind"
#   ###############################################################
		isInstructor = False
		
		# check to see if at least one class is selected
		enrolled = False
		Ccount = Course.query().count()
		for i in range(1, Ccount+1):
			if(self.request.get(str(i))):
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
				
				Ccount = Course.query().count()
				for i in range(1, Ccount+1):
					if(self.request.get(str(i))):
						u.classes.append(self.request.get(str(i)))
						c = Course.query(Course.id == i)
						course = c.get()
						course.classlist.append(u.email)
						course.put()
						time.sleep(.1)
				error = ""
				u.put()
				return self.redirect('/success')
		
		# Form not filled out fully
		else:
			error = "Please fill in every text box and select at least one class."
			return self.redirect('/signup')


# ##############################################################################################################################################
#	This of for links to the home page
#	if there is a current user it removes them
class goHome(webapp2.RequestHandler):
	def get(self):
		if self.request.cookies.get('uname'):
			self.response.delete_cookie('uname')
		global error
		error = ""
		addedQuestion = ""
		question_class = ""
		self.redirect('/home')
	
	def post(self):
		global error
		if self.request.cookies.get('uname'):
			self.response.delete_cookie('uname')
		error = ""
		addedQuestion = ""
		question_class = ""
		self.redirect('/home')
		
		
# ##############################################################################################################################################		
#	After a user is successfully created from the sign up page
class SuccessHandler(webapp2.RequestHandler):
	def get(self):
		global error
		error = ""
		template = JINJA_ENVIRONMENT.get_template('success.html')
		self.response.write(template.render())
		
		
# ##############################################################################################################################################		
#	login page
class LoginHandler(webapp2.RequestHandler):
	def get(self):
	
# #####using unused global variable in template for comparison purposes during deletion from FAQ so we don't lose class name#################
		global error 
		error = " "
# ################################################################################################################

		if self.request.cookies.get('uname'):
			usr = self.request.cookies.get('uname')
			usr = User.query(User.email==usr).fetch()
			usr = usr[0]
			questions = Questions.query().fetch()
			numClasses = len(usr.classes)
			if usr.isInstructor == True:
				template = JINJA_ENVIRONMENT.get_template('Faculty_landing.html')
				self.response.write(template.render({'user':usr, 'classes':numClasses, 'questions':questions, 'added':addedQuestion,
													'question_class':question_class}))
				
			else:
				template = JINJA_ENVIRONMENT.get_template('student_landing.html')
				self.response.write(template.render({'classClicked':classClicked, 'user':usr, 'classes':numClasses, 'questions':questions, 
													'added':addedQuestion, 'question_class':question_class}))
		else:
			self.redirect('/home')
	
	def post(self):   
		self.redirect('/login')
			
# ###########################################################################################################################################		
#	This is where changing user passwords happens			
class changePassword(webapp2.RequestHandler):
	def get(self):
		addedQuestion = ""
		question_class = ""
		self.redirect('/login')
	
	def post(self):
		global question_class, addedQuestion
		if self.request.get("oldpassword") and self.request.get("newpassword") and self.request.get("confirmnewpassword"):
			if self.request.get("oldpassword") != u.password:
				addedQuestion = "Incorrect old password input!"
				question_class = ""
				return self.redirect('/login')
											
			elif self.request.get("newpassword") == self.request.get("confirmnewpassword"):
				u.password = self.request.get("newpassword")
				u.put()
				addedQuestion = "Your password has been changed!"
				question_class = ""
				return self.redirect('/login')
			else:
				addedQuestion = "New passwords don't match "
				question_class = ""
				return self.redirect('/login')
		else:
			addedQuestion = ""
			question_class = ""
			self.redirect('/login')
	
# ##############################################################################################################################################		
#	This is where adding a question to the datastore gets done
class addQ(webapp2.RequestHandler):
	def get(self):
		global addedQuestion, question_class
		addedQuestion = ""
		question_class = ""
		self.redirect('/login')
	
	def post(self):
		global question_class, addedQuestion
		newQ = self.request.get("new-question")
		question_class = self.request.get("add-new-question")
                        
		if self.request.get("new-question"):
			#global Qcount
			Qcount = Questions.query().count() + 1
			Q = Questions(question = newQ, classQ = question_class, answer = "", id = Qcount, asker = self.request.cookies.get('uname'), timestamp = datetime.now() , timestampanswered = None)
			Q.put()
			time.sleep(0.1)
			addedQuestion = "You're question has been added to the list of questions for "
			return self.redirect('/login')
                                
		else:
			addedQuestion = "You have to ask a question for someone to be able to answer it!"
			question_class = ""
			return self.redirect('/login')

# ##############################################################################################################################################		
#	Questions get answered in this class
class answerQ(webapp2.RequestHandler):
	def get(self):
		global addedQuestion, question_class
		addedQuestion = ""
		question_class = ""
		self.redirect('/login')
	
	def post(self):
		global addedQuestion, question_class
		#question_class = self.request.get("new-entry")
		
		if self.request.get("question") and self.request.get("answer"):
			q_id = self.request.get("question")
			Q = Questions.query(Questions.id == int(q_id))
			q = Q.get()
			q.answer = self.request.get("answer")
			q.timestampanswered = datetime.now()
			if self.request.get("Add_to_FAQ"):
				q.inFAQ = True
				addedQuestion = "The question has been answered and added to the FAQ"
				q.put()
			else:
				addedQuestion = "The question has been answered"
				q.put()
			time.sleep(0.1)
			self.redirect('/login')
			
# ##############################################################################################################################################		
#	view the correct questions on the login page			
class viewQuestions(webapp2.RequestHandler):
	def get(self):
		self.redirect('/login')
	
	def post(self):
		global classClicked
		classClicked = self.request.get('class-clicked')
		self.redirect('/login')
	


# ###############################################################################################################################################
# Admin Page
class AdminHandler(webapp2.RequestHandler):
	def get(self):
		if self.request.cookies.get('uname'):
			template = JINJA_ENVIRONMENT.get_template('admin.html')
			self.response.write(template.render({'added':addedQuestion}))
		else:
			self.redirect('/home')


# #####################################################################################################################################################
class addClass(webapp2.RequestHandler):
	def get(self):
		self.redirect('/home')
	def post(self):
		global addedQuestion
		Ccount = Course.query().count()
		if self.request.get('num'):
			classes = Course.query().fetch()
			Ccount += 1
			dup = False
			name = self.request.get('subject') + ' ' + self.request.get('num')
			for c in classes:
				if c.name == name:
					dup = True
					break
			
			if dup == True:
				addedQuestion = "That class already exists"
				self.redirect('/admin')
			else:
				C = Course(subject = self.request.get('subject'), name = (self.request.get('subject') + ' ' + self.request.get('num')),
							id = Ccount)
				C.put()
				time.sleep(.5)
				addedQuestion = "Class successfully added to the system"
				self.redirect('/admin')
		

# ##############################################################################################################################################
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
			
		Courses = Course.query()
		for c in Courses:
			c.key.delete()
		time.sleep(.2)
		self.redirect('/signup')
# ##############################################################################################################################################		
# This handler displays a list of all courses. 
class PublicFAQHandler(webapp2.RequestHandler):
	def get(self): 
		# Get a list of *all* courses; pass it to the template.
		course_list = Course.query().fetch()
		template = JINJA_ENVIRONMENT.get_template('public-FAQ.html')
		self.response.write(template.render({'courses' : course_list}))

# ##############################################################################################################################################
# This handler displays an individual class's FAQ page. The URL can be copied
# for an Instructor to use outside of the application. 
class ViewFAQHandler(webapp2.RequestHandler): 
	def get(self): 
		global question_class
		if self.request.cookies.get('uname'):
			usr = self.request.cookies.get('uname')
			usr = User.query(User.email==usr).fetch()
			usr = usr[0]
		else:
			usr = User()
		if error != question_class or question_class == '':
			# This is necessary to get rid of symbols in the URL and make it query-able.
			enc_course = self.request.get("co")
			question_class = urllib.unquote(enc_course)
		
		FAQ_questions = Questions.query(Questions.inFAQ == True, Questions.classQ == question_class).fetch()
		template = JINJA_ENVIRONMENT.get_template('viewFAQ.html')
		self.response.write(template.render({'questions' : FAQ_questions, 'class' : question_class, 'user':usr}))

# ##############################################################################################################################################			
#	Delete questions from the FAQ
class Delete(webapp2.RequestHandler):
	def get(self):
		self.redirect('/viewFAQ')
	def post(self):
		global error, question_class
		error = question_class
		FAQ_questions = Questions.query(Questions.inFAQ == True, Questions.classQ == question_class).fetch()
		for q in FAQ_questions:
			if self.request.get(str(q.id)):
				q.inFAQ = False
				q.put()
				time.sleep(0.1)
		self.redirect('/viewFAQ')
		
# ##############################################################################################################################################
#	Redirecting to email page
class goEmail(webapp2.RequestHandler):
	def get(self):
		emails = Email.query().order(Email.sent_date).fetch()
		template = JE.get_template('email-page.html')
		self.response.write(template.render({
			'emails': emails
		}))
		
class ViewHandler(webapp2.RequestHandler):
	def get(self):
		email_key_urlsafe = self.request.get('email')
		email = Email.get_email_from(email_key_urlsafe)
		template = JE.get_template('view.html')
		self.response.write(template.render({
			'email': email
        }))

class DeleteEmailHandler(webapp2.RequestHandler):
	def get(self):
		email_key_urlsafe = self.request.get('email')
		ndb.Key(urlsafe=email_key_urlsafe).delete()
		redirect_to_main(self.response, 'deleted email', 0.5)
		
# ##############################################################################################################################################		
#	Send emails to students so they can register
class EmailHandler(webapp2.RequestHandler):
	def get(self):
		redirect_to_main(self.response, 'ERROR !!!!!', 0.5)

	def post(self):
		from_address = 'admin@{}.appspotmail.com'.format(app_identity.get_application_id())
		to_address = filter(lambda x: x.strip(), self.request.get('to_addresses').split(';'))
		subject = self.request.get('subject')
		message = self.request.get('message')

		if not to_address or not subject or not message:
			self.redirect('/goEmail')
			return

		text_to_print = ''
		try:
			Email.send_email(from_address, to_address, subject, message)
			text_to_print = 'successfully sent email'
		except MissingRecipientsError:
			text_to_print = 'No receipients'

		redirect_to_main(self.response, text_to_print, 0.5)

# ###############################################################################################################################################
app = webapp2.WSGIApplication([
	('/', StartupHandler),
	('/home', MainHandler),
	('/signup', SignupHandler),
	('/success', SuccessHandler),
	('/login', LoginHandler),
	('/answerQ', answerQ),
	('/addQ', addQ),
	('/delete', Delete),
	('/goHome', goHome),
	('/viewQ', viewQuestions),
	('/password', changePassword),
	('/publicFAQ', PublicFAQHandler),
	('/viewFAQ', ViewFAQHandler),
	('/admin', AdminHandler),
	('/addClass', addClass),
	('/clear', ClearHandler),
	('/goEmail', goEmail),
	('/email', EmailHandler),
	('/view', ViewHandler),
	('/delete', DeleteEmailHandler)
	
], debug=True)
