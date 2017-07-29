__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'
"""
Autor: Alexsandro Façanha
Ano: 2017

Script para agendar tarefas no Linux(Ubuntu e derivados)

Para fins pedagógicos este miniprograma possui o intuito de facilitar a realização de
tarefas repetitivas através da criação de uma rotina para que uma determinada tarefa seja
executada diversas vezes em intervalos de tempo pré-programado.

"""

import time, os
import _thread as thread
from timeit import time

from database import Database
from service import Service

list_services = []
list_service_stop = []
os.chdir('/home/asfmint/mypy/schedule_tasks')

def main():
	db = Database()
	pid = os.getpid()
	db.saveLog(['<<main:begin>>', str(pid), 'running', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
	count = 0


	while True:
		setting = db.getDataSetting()
		if setting['state'] == 'stop':
			db.saveLog(['<<main:stopped>>', str(pid), 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
			break

		for serv in db.getDataServiceAll():
			# remover da lista os serviços que estiverem parados
			if serv['state'] == 'stop':
				if serv['name'] not in list_service_stop:
					db.saveLog(['<<main:service:stopped>>', 'service', serv['name'], 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
				list_service_stop.append(serv['name'])

				if serv['name'] in list_services:
					list_services.remove(serv['name'])
				continue

			if serv['name'] not in list_services:
				db.saveLog(['<<main:service:running>>', 'service', serv['name'], 'running', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
				list_services.append(serv['name'])

				if serv['name'] in list_service_stop:
					list_service_stop.remove(serv['name'])
					
				thread.start_new_thread(Service, (db.getDataService(serv['name']),))

		time.sleep(abs(setting['time']))

if __name__ == '__main__':
	main()

