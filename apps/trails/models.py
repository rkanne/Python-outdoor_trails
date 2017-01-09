from __future__ import unicode_literals
from django.db import models
import datetime
import re
import bcrypt
# import datetime

PASSWORD_REGEX = re.compile(r'^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{8,}$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$') 


# Create your models here.
class RegistrationManager(models.Manager):
    def register(self, first_name, last_name, username, email, password, confirm_password):
        message = [] 
        if len(first_name) <2 and len(last_name) <2 and  len(username) <2:
        	message.append("Your name and username should not contain fewer than 2 characters!!")
        	if len(password) == 0:
        		message.append("Password is required")
        if len(email) == 0:
            message.append("Email is required")
        elif not EMAIL_REGEX.match(email):
        	message.append("Email is not VALID!!")
        elif not PASSWORD_REGEX.match(password):
            message.append("Password is not VALID!!")
        if len(password) < 1:
        	message.append("Password cannot be blank!")
        if len(confirm_password) < 1:
        	message.append("Confirm Password cannot be blank!")
        if password != confirm_password:
        	message.append("Passwords do not match.")
        if len(message) != 0:
            return (False, message)
        else:
        	pw_hash = bcrypt.hashpw(str(password), bcrypt.gensalt())
        	registration = Users.registerMgr.create(first_name=first_name,last_name=last_name,username=username,email=email, password=pw_hash)
        	registration.save()
        return (True, registration)

class LoginManager(models.Manager):
    def login(self, username, password):
        login_message = []
        if  len(username) <1 and len(password) < 1:
            login_message.append("Username and Password cannot be blank!")
        if len(username) == 0:
            login_message.append("Username is required")
            if len(password) == 0:
                login_message.append("Password is required")
        elif not PASSWORD_REGEX.match(password):
            login_message.append("Password is not VALID!!")
        if len(login_message) != 0:
            return (False, login_message)
        else:
        	print "False======"
        	login = Users.loginMgr.filter(username=username)
        	if len(login) < 1:
        		login_message.append("User does not exist in database")
        	elif (bcrypt.checkpw(str(password),str(login[0].password))):
        		return(True, login[0])
        	else:
        		login_message.append("Password is incorrect please try again")
                return (False, login_message)

class TripsManager(models.Manager):
	def add(self, destination, description, trip_start, trip_end):
		trips_message = []
		start= trip_start
		end = trip_end
		now = unicode(datetime.date.today())

		if len(destination) == 0:
			trips_message.append("Destination is required!!")
		if len(description) == 0:
			trips_message.append("Description is required!!")
		if len(trip_start) < 1:
			trips_message.append("Please insert travel date start!!")
		if len(trip_end) < 1:
			trips_message.append("Please insert travel date end!!")
		if start < now:
			trips_message.append("Start date must be in the future!!")
		if end < now:
			trips_message.append("End date must be in the future!!")
		elif end < start:
			trips_message.append("End date should be greater than start date")
		print 'now====', type(now), now
		print 'travel_from====', start ,'travel_to====',end

		if len(trips_message) != 0:
			return (False, trips_message)
		else:
			trips_message.append("*** You have added your Trip!!! ***")
			return (True, trips_message)

class JoinsManager(models.Manager):
	def join(self):
			return (True, "true")

class StateManager(models.Manager):
	def add(self):
			return (True, "true")
class MessagesManager(models.Manager):
	def message(self):
			return (True, "true")
class CommentsManager(models.Manager):
	def comment(self):
			return (True, "true")

class Users(models.Model):
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	username = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
        registerMgr = RegistrationManager()
        loginMgr = LoginManager()
        joinsMgr = JoinsManager()

class State(models.Model):
	abbreviation = models.CharField(max_length = 255)
	state_name = models.CharField(max_length = 255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	stateMgr = StateManager()


class Trips(models.Model):
	destination = models.CharField(max_length = 255)
	description = models.TextField()
	user = models.ForeignKey(Users, null=True)
	unique_id = models.CharField(max_length = 45, null=True)
	trip_start = models.DateField()
	trip_end = models.DateField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	tripsMgr = TripsManager()

class Join(models.Model):
	user = models.ForeignKey(Users, models.DO_NOTHING, related_name="owner")
	trip = models.ForeignKey(Trips, models.DO_NOTHING, related_name="join")
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	joinsMgr = JoinsManager()

class Messages(models.Model):
	user = models.ForeignKey(Users, null=True)
	rating = models.IntegerField(null=True)
	message = models.TextField()
	unique_trail_id = models.CharField(max_length = 45, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	messageMgr = MessagesManager()

class Comments(models.Model):
	user = models.ForeignKey(Users, null=True)
	message = models.ForeignKey(Messages, null=True)
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)	
	commentMgr = CommentsManager()

