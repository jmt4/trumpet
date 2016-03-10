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

if __name__ == '__main__':
	import tweepy
	
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)

	'''
	Precondition: Trump tweets something insane
	...
	High Level of Algorithm:
		(1) Listen on tweet
			[a] Store data on tweet so we can find it when examining 
				non-origin accounts
			LOOP:
			[b] If less than 15 events(retweets, likes, ...) wait or sleep
			[c] If more than 15 events, enqueue users from oldest 200 events
		(2) At this point we could do some sort of depth-first or breadth-first
			search on users and explore the social graph. After exploration, 
			we can use networkx to perform some crazy graph algorithms
	'''

	twitter_id = 'realDonaldTrump'

	most_recent = api.user_timeline(screen_name=twitter_id, count=5)
	for status in most_recent:
		if is_retweet(status):
			print "not original", get_original_tweet_id(status)
		else:
			print "original", get_original_tweet_id(status)
	# Status.id gives the id of the tweet but this can be a real tweet or retweet

	#print api.retweeters(first.in_reply_to_status_id)
	#for status in most_recent:
	#	print api.retweeters(int(status.id))