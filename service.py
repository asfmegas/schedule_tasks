__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'

import os
from timeit import time

from database import Database
from constants import *

os.chdir('/home/asfmint/mypy/schedule_tasks')

class Service:
	def __init__(self, data):
		self.data = data
		self.main()

	def main(self):
		count = 0
		db = Database()
		while True:
			serv = db.getDataService(self.data['name'])
			if serv['state'] == 'stop':
				db.saveLog(['<<service:stopped>>', serv['name'], 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
				break

			if serv['notice'] == 'yes':
				notice = ' '.join(['notify-send -t 6000 -i /home/asfmint/mypy/schedule_tasks/img/logo_info.png', '"Serviço [ {} ] em execução."'.format(serv['name'])])
				os.system(notice)
				db.saveLog(['<<service:running>>', serv['name'], 'running', str(serv['count']), str(serv['time']), str(time.strftime('%d/%m/%Y-%H:%M:%S'))])

			os.system(serv['command'])

			if serv['count'] > -1:
				count += 1
				if count == serv['count']:
					serv['state'] = 'stop'
					db.saveService(serv)
					break

			time.sleep(MINUTE * abs(serv['time']))
