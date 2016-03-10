import tweepy
from tweepy.api import API

try:
	import sys, os
	sys.path.insert(1, os.path.join(sys.path[0], '..'))
	from local_settings import (
		consumer_key, consumer_secret, 
		access_token, access_token_secret
	)
except ImportError:
	raise("Twitter API credentials not found")

def is_retweet(status):
	'''
	Status objects that are retwe`ets have an additional node 
	called retweeted_status.
	'''
	try:
		status.retweeted_status
		return True
	except AttributeError:
		return False

def get_original_tweet_id(status):
	'''
	Return the id of user where tweet originated
	'''
	if is_retweet(status):
		return status.retweeted_status.id
	else:
		return status.id

def is_trump_tweet(status):
	print status.user.screen_name

class UserResponseListener(tweepy.StreamListener):
	"""
	A simple stream listener extension which acts like an event handler.

	REST calls are limited, so instead stream and filter on a user handle.
	When a tweet is made (ignoring RT's, and @'s) we can snag the tweet id, 
	and monitor activity on the social network.


	Attributes
	----------

	Paramaters
	----------
	twitter_id : str
		Numeric ID of Twitter user. Something like status.user.id
	twitter_sn : str
		The screen name of Twitter user. 
		Returned with status.user.screen_name
	api : API()
		I guess this can be given to a Tweepy listener. 
		Just using thee default here

	Example
	-------
	>>> user = api.get_user('someScreenName')
	>>> ssn_listener = UserResponseListener(twitter_id=user.id)
	...
	>>> ssn_listener = UserResponseListener(twitter_sn='someScreenName')
	"""


	def __init__(self, twitter_id=None, twitter_sn=None, api=None):
		self.api = api or API()
		self.twitter_id = twitter_id
		self.twitter_sn = twitter_sn

	def on_status(self, status):
		if self.is_trump(status):
			print status.text

	@property
	def get_twitter_id(self):
		return '{}'.format(api.get_user(screen_name=self.twitter_id))

	def is_trump(self, status):
		""" Check if tweet was made by Trump """
		return self.twitter_id == status.user.screen_name

	def is_response_to_trump(self, status, tweet_id):
		'''
		
		'''
		return status.retweeted_status.id == tweet_id

if __name__ == '__main__':
	'''
	Notes:
	(1). To find the screen name of the person (re)tweeting, we can do something
		 like status.user.screen_name
	(2). Scenario: X tweets something and Y retweets it. We can find out who X is
		 from Y's retweet by something like status.retweeted_status.user.screen_name
	'''


	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	twitter_sn = 'realDonaldTrump'
	twitter_user = api.get_user(screen_name=twitter_sn)
	#twitter_id = 'EricTrump'

	#recent = api.user_timeline(screen_name=twitter_sn, count=40)
	#print recent[1]._json
	#for idx, status in enumerate(recent):
	#	print idx
	#	is_trump_tweet(status)

	#EricTrumpTweet = recent[]

	tsl = TrumpStreamListener(twitter_sn)

	tsl_stream = tweepy.Stream(auth=api.auth, listener=tsl)

	tsl_stream.filter(follow=['{}'.format(twitter_user.id)])