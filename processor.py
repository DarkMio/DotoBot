class processor(object):
	'''This is the general object to process threads. It will I/O threads,
		make nice replies, and take care of everything that is pre-filtered
		by the main-process of DotoBot.'''

	def __init__(self):
		self.comment = "This could be your average comment."

		self.disclaimer = "\n\n---\n\n^This ^is ^a ^bot ^and ^won't ^answer ^to ^mails. ^Mail ^the ^[[Botowner](http://www.reddit.com/message/compose/?to=DarkMio&amp;subject=BotReport)] ^instead. ^v0.4 ^| ^[Changelog](http://redd.it/29f2ah)"


	def index_reddit(self, submission):
		'''This should check a submission and index it into the database.'''











	def update_reddit(self, textbody):
		pass

	def wikify_it(self, textbody):
		pass