import tweet
import listen
import address_resolution

SUBNETS_FILE = "Subnets.txt"

class EditBot():
	def __init__(self):
		self.tweeter = tweet.TweetHandler()
		self.listener = listen.WikipediaListener(self.edit_callback)
		self.address_resolver = address_resolution.SubnetHandler(SUBNETS_FILE)
		self.edit_count = 0
		self.tweet_count = 0

	def start(self):
		self.listener.start()

	def edit_callback(self, edit):
		self.edit_count += 1
		location = self.address_resolver.name_for_address(edit.user)
		if location is not None:
			self.tweet_count += 1
			tweet = "'%s' edited from %s @UChicago %s" % (edit.page_title, location, edit.url)
			if len(tweet) > 140:
				tweet = "'%s' edited from @UChicago %s" % (edit.page_title, edit.url)
			self.tweeter.send_tweet(tweet)
		if self.edit_count % 1000 == 0:
			print "Edit count: %s, Tweet count: %s" % (str(self.edit_count), str(self.tweet_count))

if __name__ == "__main__":
	bot = EditBot()
	bot.start()
