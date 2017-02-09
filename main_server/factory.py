from user import user
from config import conf
users={} #{token:user}

def create_user(username,password): #not implement
	"""verify username and password. if it's valid create a user object and put that into users"""
	return user("dasdsd",conf.BAIDU)

def get_user(token): #not implement
	"""verify the validity of the token. return a user object in users if it's valid or
	   or an error if it's not."""
	return user(token,conf.BAIDU)

def remove_user(token): #not implement
	"""remove user form users according token, return true if succeeding false if it's not"""
	pass