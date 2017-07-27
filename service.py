__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'

import time, os

from database import Database

class Service:
	def __init__(self, data):
		self.data = data
		self.main()

	def setData(dataService):
		self.data = dataService

	def main(self):
		count = 0
		db = Database()
		while True:
			serv = db.getDataService(self.data['name'])
			if serv['state'] == 'stop':
				break

			os.system(serv['command'])

			if serv['count'] > -1:
				count += 1
				if count == serv['count']:
					serv['state'] = 'stop'
					db.saveService(serv)
					break

			time.sleep(60 * serv['time'])
