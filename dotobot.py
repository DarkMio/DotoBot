import praw
from ConfigParser import ConfigParser
from time import time
from database import database
import log

from pprint import pprint

class dotobot(object):

	def __init__(self):
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
		

		self.db = database()


		self.flairs_submission = ["Soundmod", "Iconmod", "Heromod", "Announcer", "Gamemode", "Map", "Software"]
		self.flairs_update = ["Update"]
		self.flairs_good = self.flairs_submission + self.flairs_update


		with open('comments/index_comment.txt', 'r') as f:
			self.index_comment = f.read()
		with open('comments/update_comment.txt', 'r') as f:
			self.update_comment = f.read()

	def tasklist_worker(self, age):
		task = self.db.load_tasklist(age)
		for column in task:
			submission = self.r.get_submission(submission_id=column[1])
			if any(str(submission.link_flair_text) in s for s in self.flairs_good):
				if banned_by:
					# If a submission is deleted by a moderator, the bot will skip it.
					self.db.update_flair('deleted', submission.id)
					continue
				if submission.approved_by and age == 0:
					if any(str(submission.link_flair_text) in s for s in self.flairs_submission):
						# if a submission fits in the index-criteria, the bot will index it.
						self.db.index_submission(submission)
						self.db.update_flair(submission.link_flair_text, submission.id)

					elif any(str(submission.link_flair_text) in s for s in self.flairs_update):
						# if a submission fit in the update-critera, the bot will update it.
						self.db.update_submission(some_vars_need_to_be_here)
				elif age == 1:
					# Do I need to send a message? How do I make that DRY?
					msg = self.user_interaction('modmsg', submission.id, submission.title)
					self.r.send_message('/r/dota2modding', 'No flaired content!', msg)
					self.db.messaged_moderator(some_vars_go_here)
				else:
					pass
			elif submission.link_flair_text == None and column[4]:
				self.r_send_message(submission.author, 'Title goes here.', 'message goes here')
				self.db.update_messaged_user(vars_goes_here)
			else:
				self.db.flair_crap(vars_goes_here)
		self.tasklist_worker(1)

	def user_interaction(self, text_type, shortlink, rand_int=None, title=None):
		'''Loads responses and builds some, based on the content-need.'''
		# depricated
		if text_type == 'index':
			with open('comments/index_comment.txt', 'r') as f:
				index_comment = f.read()
			cmt = index_comment.format(rand_int, shortlink)
			return cmt
		
		if text_type == 'update':
			with open('comments/update_comment.txt', 'r') as f:
				update_comment = f.read()
			cmt = update_comment.format(shortlink)
			return cmt

		if text_type == 'modmsg':
			with open('comments/mod_msg.txt', 'r') as f:
				mod_msg = f.read()
			msg = mod_msg.format(shortlink, title)
			return msg

		if text_type == 'usrmsg':
			with open('comments/usr_msg.txt', 'r') as f:
				mod_msg = f.read()
			msg = mod_msg.format(shortlink, title)
			return msg



	def index_submission(self, submission):
		'''This should check a submission and index it into the database.'''

		logger.info('Indexing %s in database.')
		sid = randint(10000000, 99999999)
		try:
			db.write_submission(submission.author, submission.id, submission.title, submission.selftext, submission.link_flair_text, sid)
		except mysql.MySQLError, err:
			logger.error('Failed at indexing {0} in database, following reason was given:'.format(submission.id))
			logger.error(str(err))

		reply = self.index_comment.format(sid, submission.id)
		return reply


	def update_reddit(self, submission):
		logger.info('Loading all entries from /u/{0}'.format(submission.author))
		db.query('')


	def wikify_it(self, textbody):
		pass


class db_worker(object):
	'''db_worker takes care of the maintance of the database,
		additionally he writes out the JSON for the mod-database
		and helps us splitting I/O aswell as interfacing with the DB.'''

	def __init__(self):
		# How JSON should look like: [{usr, shortlink, descr, content, type}, {}, {},]



if __name__ == "__main__":
	logger = log.setup_custom_logger('root')

	bot = dotobot()

	#bot.tasklist_worker(0)

	print bot.user_interaction('usrmsg', '2ctqx5', title='This is some title.')