# This code is sloppy and just retries itself without printing any error.
# This works well for a hosted python server, but shouldn't be used on a
# dev-machine, since you will get no errors.
# This bot usually gets after a few hours for a few seconds in trouble,
# restarting one of the streams. That is a connection-error of reddit,
# just ignore it.
# Have fun.


import praw
import datetime
import random
import sqlite3
import threading
import re
import logging
import traceback
import urllib2
import argparse
from ConfigParser import ConfigParser

from time import time, sleep

class multithread(object):

	def __init__(self):
		self.running = True
		self.threads = []


		config = ConfigParser()
		config.read('config.ini')

		descr = config.get('REDDIT', 'descr')
		subreddit = config.get('REDDIT', 'subreddit')

		usr = config.get('LOGIN', 'usr')
		pwd = config.get('LOGIN', 'pwd')

		self.r = praw.Reddit(user_agent=descr)
		self.r.login(usr, pwd)

		self.subreddit = subreddit
		self.now = int(time())
		# best handling without formatting is to not format it.

		self.comment = "Here could be your comment."



	def submission_stream(self):
		"""Checks all submissions. Either they're link.posts or self.posts. Either way, we catch both."""
		while True:

			try:
				submission_stream = praw.helpers.submission_stream(self.r, self.subreddit, limit=None, verbosity=0)
				log.info("Opened submission stream successfully.")
				while self.running == True:
					submission = next(submission_stream) # retrieve the next submission

					if (submission.approved_by
						and not check(submission.id)
						):
						p.index_reddit(submission)



			except:
				log.info("Submission stream broke. Retrying in 60.")
				log.debug(traceback.print_exc())
				sleep(60)
				pass
			

	def database_cleaner(self):
		"""Cleans up the database, which contains worked-through IDs."""
		while self.running == True:

			deleteme = cur.execute("SELECT * FROM reddit WHERE time + 86400 < %s" % self.now)
			i = 0
			if deleteme:
				for i, entry in enumerate(cur.fetchall()):
					cur.execute("DELETE FROM reddit WHERE id = '%s'" % entry[1])
					i += 0
				i > 0 and log.info("Cleaned %s entries from the database." % i)

			sleep(3600)


	def close(self):
		db.close()
		log.error("CRITICAL ERROR:")
		log.debug(traceback.print_exc())
		log.info("Established connection to database was closed.")
		raise SystemExit


	def go(self):
		t1 = threading.Thread(target=self.comment_stream)
		t2 = threading.Thread(target=self.submission_stream)
		t3 = threading.Thread(target=self.database_cleaner)
		# Make threads daemonic, i.e. terminate them when main thread
		# terminates. From: http://stackoverflow.com/a/3788243/145400
		t1.daemon = True
		t2.daemon = True
		t3.daemon = True
		t1.start()
		t2.start()
		t3.start()
		self.threads.append(t1)
		self.threads.append(t2)
		self.threads.append(t3)


def join_threads(threads):
	"""
	Join threads in interruptable fashion.
	From http://stackoverflow.com/a/9790882/145400
	"""
	for t in threads:
		while t.isAlive():
			t.join(5)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='DotoBot deals with database and moderation-processes in /r/Dota2Modding.')
	parser.add_argument('--verbose', action='store_true', help='Print mainly tracebacks.')
	args = parser.parse_args()

	# SET UP LOGGER
	logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%X', level=logging.DEBUG if args.verbose else logging.INFO)
	log = logging.getLogger(__name__)
	log.addFilter(NoParsingFilter())

	# SET UP DATABASE
	db = sqlite3.connect('massdrop.db', check_same_thread=False, isolation_level=None)
	cur = db.cursor()

	t = multithread()

	t.go()
	try:
		join_threads(t.threads)
	except KeyboardInterrupt:
		log.info("Stopping process entirely.")
		db.close() # you can't close it enough, seriously.
		log.info("Established connection to database was closed.")