from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register(self, first, last, username, email, dob, password, confirm):
		response = {
			"valid": True,
			"errors": [],
			"user": None
		}

		if len(first) < 1:
			response["errors"].append("First name is required")
		elif len(first) < 2:
			response["errors"].append("First name must be 2 characters or longer")

		if len(last) < 1:
			response["errors"].append("Last name is required")
		elif len(last) < 2:
			response["errors"].append("Last name must be 2 characters or longer")

		if len(username) < 1:
			response["errors"].append("Username is required")
		elif len(username) < 3:
			response["errors"].append("Username must be 3 characters or longer")

		if len(email) < 1:
			response["errors"].append("Email is required")
		elif not EMAIL_REGEX.match(email):
			response["errors"].append("Invalid Email")
		else:
			email_list = User.objects.filter(email=email.lower())
			if len(email_list) > 0:
				response["errors"].append("Email is already in use")

		if len(dob) < 1:
			response["errors"].append("Date of Birth is required")
		else:
			date = datetime.strptime(dob, '%Y-%m-%d')
			today = datetime.now()
			if date > today:
				response["errors"].append("Date of Birth must be in the past")

		if len(password) < 1:
			response["errors"].append("Password is required")
		elif len(password) < 8:
			response["errors"].append("Password must be 8 characters or longer")

		if len(confirm) < 1:
			response["errors"].append("Confirm Password is required")
		elif confirm != password:
			response["errors"].append("Confirm Password must match Password")

		if len(response["errors"]) > 0:
			response["valid"] = False
		else:
			response["user"] = User.objects.create(
				first_name=first,
				last_name=last,
				username=username,
				email=email.lower(),
				dob=date,
				password=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
			)

		return response

	def login(self, email, password):
		response = {
			"valid": True,
			"errors": [],
			"user": None
		}

		if len(email) < 1:
			response["errors"].append("Email is required")
		elif not EMAIL_REGEX.match(email):
			response["errors"].append("Invalid Email")
		else:
			email_list = User.objects.filter(email=email.lower())
			if len(email_list) == 0:
				response["errors"].append("Unknown email")

		if len(password) < 1:
			response["errors"].append("Password is required")
		elif len(password) < 8:
			response["errors"].append("Password must be 8 characters or longer")

		if len(response["errors"]) == 0:
			hashed_pw = email_list[0].password
			if bcrypt.checkpw(password.encode(), hashed_pw.encode()):
				response["user"] = email_list[0]
			else:
				response["errors"].append("Incorrect Password")

		if len(response["errors"]) > 0:
			response["valid"] = False

		return response

class MessageManager(models.Manager):
	def sendMessage(self, content, sent_by, received_by):
		print content
		if len(content) > 0:
			message = Message.objects.create(
				content=content,
				sent_by_id=sent_by,
				received_by_id=received_by
			)
			return message
		else:
			return "Message cannot be blank!"

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	dob = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Message(models.Model):
	content = models.TextField(max_length=1000)
	sent_by = models.ForeignKey(User, related_name="sent_messages")
	received_by = models.ForeignKey(User, related_name="received_messages")
	created_at = models.DateTimeField(auto_now_add=True)
	objects = MessageManager()