import tweet
import listen
import address_resolution

SUBNETS_FILE = "subnets.txt"

class EditBot():
	def __init__(self):
		self.tweeter = tweet.TweetHandler()
		self.listener = listen.WikipediaListener(self.edit_callback)
		self.address_resolver = address_resolution.SubnetHandler(SUBNETS_FILE)

	def start(self):
		self.listener.start()

	def edit_callback(self, edit):
		location = self.address_resolver.name_for_address(edit.user)
		if location is not None:
			tweet = "'%s' edited from %s @UChicago %s" % (edit.page_title, location, edit.url)
			self.tweeter.send_tweet(tweet)

if __name__ == "__main__":
	bot = EditBot()
	bot.start()
