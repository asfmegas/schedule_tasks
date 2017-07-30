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
	db.saveLog(['<<main:begin>>', str(pid), 'running', str(time.strftime('%d/%m/%Y-%H:%M:%S')), '<<main:begin>>'])
	os.system('notify-send -t 8000 -i /home/asfmint/mypy/schedule_tasks/img/logo_info.png "Schedule Tasks" "Agende suas tarefas e torne seu trabalho mas fácil."')
	count = 0

	while True:
		setting = db.getDataSetting()
		if setting['state'] == 'stop':
			db.saveLog(['<<main:stopped>>', str(pid), 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
			break

		for serv in db.getDataServiceAll():
			# remover da lista os serviços que estiverem parados
			if serv['state'] == 'stop':
				# verifica se o serviço não está na lista para realizar um registro
				if serv['name'] not in list_service_stop:
					# registro
					db.saveLog(['<<main:service:stopped>>', 'service', serv['name'], 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
					list_service_stop.append(serv['name']) # adiciona o serviço com status de stop a lista de serviços parados
					
				# db.saveLog(['debug'] + list_service_stop)
				# verifica se o serviço está na lista
				if serv['name'] in list_services:
					# remove da lista de serviços que serão iniciados
					list_services.remove(serv['name'])
				continue

			# verifica se o serviço está na lista para ser iniciado
			if serv['name'] not in list_services:
				# registro
				db.saveLog(['<<main:service:start>>', 'service', serv['name'], 'start', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
				list_services.append(serv['name']) # adiciona serviço na lista

				# verifica se o serviço está na lista de serviços parados
				if serv['name'] in list_service_stop:
					list_service_stop.remove(serv['name']) # remove serviço da lista
				
				# cria uma thread com um novo serviço
				thread.start_new_thread(Service, (db.getDataService(serv['name']),))

		time.sleep(abs(setting['time']))

if __name__ == '__main__':
	main()

