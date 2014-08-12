import MySQLdb as mysql
from ConfigParser import ConfigParser
import logging
import log


logger = logging.getLogger('root')

class database(object):
	'''The general database object. It should care about all interactions with the database.'''

	def __init__(self):
		config = ConfigParser()
		config.read('config.ini')


		host = config.get('DATABASE', 'host')
		user = config.get('DATABASE', 'user')
		pwd  = config.get('DATABASE', 'pwd')
		db = config.get('DATABASE', 'db')

		self.con = mysql.connect(host, user, pwd, db)
		self.cur = self.con.cursor()
		self.con.set_character_set('utf8')
		self.cur.execute('SET NAMES utf8')
		self.cur.execute('SET CHARACTER SET utf8')
		self.cur.execute('SET character_set_connection=utf8')
		# Commit VALUE if written. Otherwise it will just vanish. :(
		self.con.autocommit(True)
		logger.info("Established a connection to the database.")

	def write_submission(self, user, shortlink, description, content, modtype, sid):
		'''This function writes submission into the live moddatabase.'''
		self.cur.execute('INSERT INTO moddb VALUE (UNIX_TIMESTAMP(now()), %s, %s, %s, %s, %s, %s);', [user, shortlink, description, content, modtype, sid])
		logger.info('Written {0} successfully in main database.'.format(shortlink))
		# if you can write it in the database, then store it in the tasklist aswell
		self.delete_tasklist(shortlink)
		return

	def write_watchlist(self, shortlink):
		'''This function writes the shortlink of a submission after the task is done.'''
		self.cur.execute('INSERT INTO watchlist VALUE (UNIX_TIMESTAMP(now()), ?);', (shortlink, ))
		logger.info('Written {0} successfully in taskdione.'.format(shortlink))
		return

	def check_watchlist(self, submission_id):
		if self.cur.execute('SELECT * FROM watchlist WHERE shortlink = %s LIMIT 1;', [submission_id]):
			return True

	def load_tasklist(self, age):
		if age == 0:
			self.cur.execute('SELECT * FROM tasklist WHERE timestamp < (unix_timestamp(now()) - 1800) AND timestamp > (unix_timestamp(now()) - 86400) AND flaired IS NULL;')
			data = self.cur.fetchall()
			return data
		if age == 1:
			self.cur.execute('SELECT * FROM tasklist WHERE timestamp < (unix_timestamp(now()) - 86400) AND flaired IS NULL;')
			data = self.cur.fetchall()
			return data

	def delete_tasklist(self, shortlink):
		self.cur.execute('DELETE FROM tasklist WHERE shortlink = %s', [shortlink])
		logger.info('Deleted entry with ID {0}.'.format(shortlink))

	def messaged_moderator(self, shortlink):
		if self.cur.execute('SELECT * FROM tasklist WHERE shortlink = %s', [shortlink]):
			self.cur.execute('UPDATE tasklist SET mailed = "mod" WHERE shortlink = %s', [shortlink])
			logger.info('Updated mailstatus of shortlink {0} to "mod".'.format(shortlink))
		else:
			# This should never, ever happen. Or else the flow from the function-request is broken.
			raise KeyError('Shortlink {0} is not valid and has not been found in the database.'.format(shortlink))
		return

	def update_messaged_user(self, shortlink):
		if self.cur.execute('SELECT * FROM tasklist WHERE shortlink = %s', [shortlink]):
			self.cur.execute('UPDATE tasklist SET mailed = "usr" WHERE shortlink = %s', [shortlink])
			logger.info('Updated mailstatus of shortlink {0} to "usr".'.format(shortlink))

	def update_flaired(self, shortlink, flair):
		self.cur.execute('UPDATE tasklist SET flaired = %s WHERE shortlink = %s', [flair, shortlink])
		logger.info('Set the flair for ID {0} to {1}.'.format(shortlink, flair))
	def clear_tasklist(self):
		self.cur.execute('DELETE FROM tasklist WHERE timestamp > unix_timestamp(now()) - 2592000;')


if __name__ == '__main__':
	logger = log.setup_custom_logger('root')
	db = database()
	#print db.load_tasklist(0)
	db.messaged_moderator('thisisnovalidshortlink')