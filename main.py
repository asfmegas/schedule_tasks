__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'

import time
import _thread as thread

from database import Database
from service import Service

list_services = []

def main():
	db = Database()
	count = 0
	while True:
		setting = db.getDataSetting()
		for s in db.getDataServiceAll():
			# remover da lista os serviços que estiverem parados
			# print('antes: ', list_services) # Apenas debug
			if s['state'] == 'stop':
				if s['name'] in list_services:
					list_services.remove(s['name'])
				continue

			if s['name'] not in list_services:
				list_services.append(s['name'])
				thread.start_new_thread(Service, (db.getDataService(s['name']),))
			# print('depois:', list_services) # apenas debug

		if setting['state'] == 'stop':
			break
		time.sleep(setting['time'])

if __name__ == '__main__':
	main()

