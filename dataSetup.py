import os
import pprint
from google.appengine.api import memcache
from google.appengine.api import mail
from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from datetime import datetime

pprint.pprint(os.environ.copy())

class Questions(ndb.Model):
	question = ndb.StringProperty()
	answer = ndb.StringProperty()
	classQ = ndb.StringProperty()
	inFAQ = ndb.BooleanProperty()
	id = ndb.IntegerProperty()
	asker = ndb.StringProperty()
	timestamp = ndb.DateTimeProperty(auto_now = True)
	
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
	classes = ndb.StringProperty(repeated=True)

def create_courses():
	course1 = Course()
	course1.classlist = ['JianChiang@gmail.com', 'AdaJJohnson@gmail.com', 'IsoldeVinogradova@gmail.com']
	course1.name = 'PHYS 498'
	course1.subject = 'PHYS'
	course1.id = 1

	course2 = Course()
	course2.classlist = ['MaryMCourt@gmail.com', 'JustinoAlcantar@gmail.com', 'AdaJJohnson@gmail.com', 'GhazwanMustafa@gmail.com']
	course2.name = 'COMPSCI 347'
	course2.subject = 'COMPSCI'
	course2.id = 2

	course3 = Course()
	course3.classlist = ['JianChiang@gmail.com', 'JustinoAlcantar@gmail.com', 'IsoldeVinogradova@gmail.com']
	course3.name = 'COMPSCI 404'
	course3.subject = 'COMPSCI'
	course3.id = 3

	course4 = Course()
	course4.classlist = ['MaryMCourt@gmail.com', 'JustinoAlcantar@gmail.com', 'GhazwanMustafa@gmail.com', 'IsoldeVinogradova@gmail.com']
	course4.name = 'ANTHRO 205'
	course4.subject = 'ANHTRO'
	course4.id = 4

	course5 = Course()
	course5.classlist = ['MaryMCourt@gmail.com', 'JianChiang@gmail.com', 'JustinoAlcantar@gmail.com', 'GhazwanMustafa@gmail.com']
	course5.name = 'MATH 318'
	course5.subject = 'MATH'
	course5.id = 5

	course1.put()
	course2.put()
	course3.put()
	course4.put()
	course5.put()

def create_users():
	user1 = User()
	user1.Fname = 'Mary'
	user1.Lname = 'Court'
	user1.email = 'MaryMCourt@gmail.com'
	user1.password = 'password'
	user1.isInstructor = False
	user1.classes = ['COMPSCI 347', 'MATH 318', 'ANTHRO 205']

	user2 = User()
	user2.Fname = 'Jian'
	user2.Lname = 'Chiang'
	user2.email = 'JianChiang@gmail.com'
	user2.password = 'password'
	user2.isInstructor = False
	user2.classes = ['COMPSCI 404', 'PHYS 498', 'MATH 318']

	user3 = User()
	user3.Fname = 'Justino'
	user3.Lname = 'Alcantar'
	user3.email = 'JustinoAlcantar@gmail.com'
	user3.password = 'password'
	user3.isInstructor = False
	user3.classes = ['MATH 318', 'COMPSCI 347', 'COMPSCI 404', 'ANTHRO 205']

	user4 = User()
	user4.Fname = 'Ada'
	user4.Lname = 'Johnson'
	user4.email = 'AdaJJohnson@gmail.com'
	user4.password = 'password'
	user4.isInstructor = False
	user4.classes = ['PHYS 498', 'COMPSCI 347']

	user5 = User()
	user5.Fname = 'Ghazwan'
	user5.Lname = 'Mustafa'
	user5.email = 'GhazwanMustafa@gmail.com'
	user5.password = 'password'
	user5.isInstructor = False
	user5.classes = ['COMPSCI 347', 'ANTHRO 205', 'MATH 318']

	user6 = User()
	user6.Fname = 'Isolde'
	user6.Lname = 'Vinogradova'
	user6.email = 'IsoldeVinogradova@gmail.com'
	user6.password = 'password'
	user6.isInstructor = False
	user6.classes = ['PHYS 498', 'COMPSCI 404', 'ANTHRO 205']

	teacher1 = User()
	teacher1.Fname = 'Flora'
	teacher1.Lname = 'Marchesi'
	teacher1.email = 'FloraMarchesi@gmail.com'
	teacher1.password = 'password'
	teacher1.isInstructor = True
	teacher1.classes = ['PHYS 498']

	teacher2 = User()
	teacher2.Fname = 'Allan'
	teacher2.Lname = 'Lewis'
	teacher2.email = 'AllanTLewis@gmail.com'
	teacher2.password = 'password'
	teacher2.isInstructor = True
	teacher2.classes = ['ANTHRO 205']

	teacher3 = User()
	teacher3.Fname = 'Gretchen'
	teacher3.Lname = 'Chastain'
	teacher3.email = 'GretchenPChastain@gmail.com'
	teacher3.password = 'password'
	teacher3.isInstructor = True
	teacher3.classes = ['COMPSCI 347', 'COMPSCI 404']

	teacher4 = User()
	teacher4.Fname = 'Rafaela'
	teacher4.Lname = 'Goncalves'
	teacher4.email = 'RafaelaGoncalves@gmail.com'
	teacher4.password = 'password'
	teacher4.isInstructor = True
	teacher4.classes = ['MATH 318']

	user1.put()
	user2.put()
	user3.put()
	user4.put()
	user5.put()
	user6.put()
	teacher1.put()
	teacher2.put()
	teacher3.put()
	teacher4.put()

def create_questions():
	question1 = Questions()
	question1.question = 'What is a natural number?'
	question1.answer = 'A natural number is any positive integer'
	question1.classQ = 'MATH 318'
	question1.inFAQ = True
	question1.id = 1
	question1.asker = 'GhazwanMustafa@gmail.com'
	question1.timestamp = datetime.now()

	question2 = Questions()
	question2.question = 'In what year was the ruin of Pompeii discovered?'
	question2.answer = '1748 by Roque Joaquin de Alcubierre'
	question2.classQ = 'ANTHRO 205'
	question2.inFAQ = True
	question2.id = 2
	question2.asker = 'MaryMCourt@gmail.com'
	question2.timestamp = datetime.now()

	question3 = Questions()
	question3.question = 'What is the time complexity of Quick Sort?'
	question3.answer = 'Quick Sort has a complexity of O(n log n) time'
	question3.classQ = 'COMPSCI 347'
	question3.inFAQ = True
	question3.id = 3
	question3.asker = 'GretchenPChastain@gmail.com'
	question3.timestamp = datetime.now()

	question4 = Questions()
	question4.question = 'What is loose class coupling?'
	question4.answer = 'A loosely coupled system is one in which each of its components has, or makes use of, little or no knowledge of the definitions of other components'
	question4.classQ = 'COMPSCI 404'
	question4.inFAQ = True
	question4.id = 4
	question4.asker = 'JustinoAlcantar@gmail.com'
	question4.timestamp = datetime.now()

	question5 = Questions()
	question5.question = 'What is cohesion?'
	question5.answer = 'Cohesion measures the strength of relationship between pieces of functionality within a given module.'
	question5.classQ = 'COMPSCI 404'
	question5.inFAQ = True
	question5.id = 5
	question5.asker = 'IsoldeVinogradova@gmail.com'
	question5.timestamp = datetime.now()

	question6 = Questions()
	question6.question = 'What is the approximate mass of a neutrino?'
	question6.answer = 'A neutrino is approximately <= 0.120 eV/c2'
	question6.classQ = 'PHYS 498'
	question6.inFAQ = True
	question6.id = 6
	question6.asker = 'IsoldeVinogradova@gmail.com'
	question6.timestamp = datetime.now()

	question1.put()
	question2.put()
	question3.put()
	question4.put()
	question5.put()
	question6.put()

create_users()
create_courses()
create_questions()