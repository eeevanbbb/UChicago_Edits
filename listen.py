import websocket
import json
from datetime import datetime

REPEAT_EDIT_MAX_TIME = 60 * 5 # 5 Minutes

# {"action": "edit", "change_size": -70, "flags": null, "hashtags": [], "is_anon": false, "is_bot": false, "is_minor": false, "is_new": false, "is_unpatrolled": false, "mentions": [], "ns": "Main", "page_title": "List of Vikings characters", "parent_rev_id": "762313049", "rev_id": "762311834", "summary": null, "url": "https://en.wikipedia.org/w/index.php?diff=762313049&oldid=762311834", "user": "TheVampire"}
class WikipediaEdit():
	def __init__(self, message):
		message_dict = json.loads(message)
		for key in message_dict:
			setattr(self, key, message_dict[key])
		self.date = datetime.now()

	def __repr__(self):
		return "Edit of page %s" % self.page_title.encode('utf-8')

	def is_repeat_of_edit(self, edit):
		return edit is not None and edit.user == self.user and edit.page_title == self.page_title and abs(self.date - edit.date) < REPEAT_EDIT_MAX_TIME


class WikipediaListener():
	def __init__(self, edit_callback):
		self.edit_callback = edit_callback

		websocket.enableTrace(True)
		self.ws = websocket.WebSocketApp("ws://wikimon.hatnote.com/en/", on_message = self.on_message, on_error = self.on_error, on_close = self.on_close)

		self.last_edit = None
		self.repeat_count = 0

	def start(self):
		self.ws.run_forever()

	def on_message(self, ws, message):
		edit = WikipediaEdit(message)
		if edit.is_anon and edit.action == "edit" and not edit.is_bot:
			if edit.is_repeat_of_edit(self.last_edit):
				self.repeat_count += 1
			else:
				self.repeat_count = 0
			self.last_edit = edit
			if self.repeat_count >= 3:
				# TODO: throttle tweet frequency
				print "Detected Repeating Edit: %s" % edit

			self.edit_callback(edit)

	def on_error(self, ws, error):
		print error

	def on_close(self, ws):
		print "### closed ###"


def print_edit(edit):
	print edit

if __name__ == "__main__":
	listener = WikipediaListener(print_edit)
	listener.start()