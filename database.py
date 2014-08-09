from ConfigParser import ConfigParser

class database(object):
	'''The general database object. It should care about all interactions with the database.'''

	def __init__(self):
		config = ConfigParser()
		config.read('config.ini')


		self.host = config.get('DATABASE', 'host')
		self.user = config.get('DATABASE', 'user')
		self.pwd  = config.get('DATABASE', 'pwd')
		self.db = config.get('DATABASE', 'sb')

		self.con = mysql.connect(self.host, self.user, self.pwd, self.db)
		self.cur = self.con.cursor()
		self.con.set_character_set('utf8')
		self.cur.execute('SET NAMES utf8')
		self.cur.execute('SET CHARACTER SET utf8')
		self.cur.execute('SET character_set_connection=utf8')
		# Commit VALUE if written. Otherwise it will just vanish. :(
		self.con.autocommit(True)
		print "> Established a connection to the database."
