import praw
from ConfigParser import ConfigParser
from pprint import pprint


config = ConfigParser()
config.read('config.ini')

descr = config.get('REDDIT', 'descr')
subreddit = config.get('REDDIT', 'subreddit')

usr = config.get('LOGIN', 'usr')
pwd = config.get('LOGIN', 'pwd')
print "Logging in."
r = praw.Reddit(user_agent=descr)
r.login(usr, pwd)
print "Logged in."

data = r.get_submission(submission_id='2d1ve8')

pprint(vars(data))