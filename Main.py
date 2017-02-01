import time
import sys

import tweet
import listen
import address_resolution

SUBNETS_FILE = "Subnets.txt"

#Prepend time to all log output (http://stackoverflow.com/questions/4883789/adding-a-datetime-stamp-to-python-print)
old_out = sys.stdout
class new_out:
    nl = True

    def write(self, x):
        """Write function overloaded."""
        if x == '\n':
            old_out.write(x)
            self.nl = True
        elif self.nl:
            old_out.write('[%s] %s' % (time.ctime(), x))
            self.nl = False
        else:
            old_out.write(x)

sys.stdout = new_out()

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
			print "Edit detected from %s" % edit.user
			self.tweet_count += 1
			tweet = "'%s' edited from %s @UChicago %s" % (edit.page_title, location, edit.url)
			if len(tweet) > 140:
				tweet = "'%s' edited from @UChicago %s" % (edit.page_title, edit.url)
			self.tweeter.send_tweet(tweet)
		if self.edit_count % 1000 == 0:
			print "Edit count: %s, Tweet count: %s" % (str(self.edit_count), str(self.tweet_count))

if __name__ == "__main__":
	print "Bot Started"
	bot = EditBot()
	bot.start()
