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

			# os.system(serv['command'])

			count += 1
			if count == serv['count']:
				break
			time.sleep(10 * serv['time'])
