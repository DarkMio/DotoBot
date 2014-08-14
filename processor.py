from random import randint
import log

class processor(object):
	'''This is the general object to process threads. It will I/O threads,
		make nice replies, and take care of everything that is pre-filtered
		by the main-process of DotoBot.'''

	def __init__(self):
		with open("submission_comment.txt", "r") as f:
			self.sub_comment = f.read()

		self.disclaimer = "\n\n---\n\n^This ^is ^a ^bot ^and ^won't ^answer ^to ^mails. ^Mail ^the ^[[Botowner](http://www.reddit.com/message/compose/?to=DarkMio&amp;subject=BotReport)] ^instead. ^v0.4 ^| ^[Changelog](http://redd.it/29f2ah)"


	def index_reddit(self, submission):
		'''This should check a submission and index it into the database.'''
		logger.info('Indexing %s in database.')
		sid = randint(10000000, 99999999)
		try:
			db.write_submission(submission.author, submission.id, submission.title, submission.selftext, submission.link_flair_text, sid)
			
		except mysql.MySQLError, err:
			logger.error('Failed at indexing {0} in database, following reason was given:'.format(submission.id))
			logger.error(str(err))

		reply = self.sub_comment.format(sid)
		return reply


	def update_reddit(self, submission):
		logger.info('Loading all entries from /u/{0}'.format(submission.author))
		db.query('')


	def wikify_it(self, textbody):
		pass

if __name__ == '__main__':
	logger = log.setup_custom_logger('root')
