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
count_debug = 0 # para debug

list_services = []
list_service_stop = []
date_started = []
os.chdir('/home/asfmint/mypy/schedule_tasks')

def checkStart(old, new, db):
	global count_debug
	to_return = False
	count_debug += 1
	# restart os serviços em estado de espera "wait"
	if old != new:
		print('old:', old, 'new:', new)
		for serv in db.getDataServiceAll():
			if serv['state'] == 'wait':
				db.saveLog(['Serviço', serv['name'], 'mandando estado de "wait" para "running"'])
				serv['state'] = 'running'
				list_services.remove(serv['name'])
				db.saveService(serv)
		to_return = True
	return to_return

def main():
	db = Database()
	pid = os.getpid()
	# guarda a data de partida
	date_started = [int(i) for i in time.strftime('%d %m').split()]
	count = 0
	
	db.saveLog(['<<main:begin>>', str(pid), 'running', str(time.strftime('%d/%m/%Y-%H:%M:%S')), '<<main:begin>>'])
	os.system('notify-send -t 8000 -i /home/asfmint/mypy/schedule_tasks/img/logo_info.png "Schedule Tasks" "Agende suas tarefas e torne seu trabalho mas fácil."')

	while True:
		setting = db.getDataSetting()
		# obtem a data atual
		if count_debug < 100: date_actual = [int(i) for i in time.strftime('%d %m').split()]
		elif count_debug >= 100 and count_debug < 200: date_actual = [2, 8]; # print([2, 8])
		elif count_debug >= 200 and count_debug < 300: date_actual = [3, 8]; # print([3, 8])
		elif count_debug >= 300 and count_debug < 400: date_actual = [4, 8]; # print([4, 8])
		elif count_debug >= 400 and count_debug < 500: date_actual = [5, 8]; # print([5, 8])
		elif count_debug >= 500 and count_debug < 600: date_actual = [6, 8]; # print([6, 8])
		else: break

		if setting['state'] == 'stop':
			db.saveLog(['<<main:stopped>>', str(pid), 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
			break

		if checkStart(date_started, date_actual, db): 
			date_started = date_actual.copy()
			print('date started:', date_started, 'date actual:', date_actual)
		for serv in db.getDataServiceAll():
			# remover da lista os serviços que estiverem parados
			if serv['state'] == 'stop':
				# verifica se o serviço não está na lista para realizar um registro
				if serv['name'] not in list_service_stop:
					# registro
					db.saveLog(['<<main:service:stopped>>', 'service', serv['name'], 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
					list_service_stop.append(serv['name']) # adiciona o serviço com status de stop à lista de serviços parados
					
				# verifica se o serviço está na lista
				if serv['name'] in list_services:
					# remove o serviço da lista de serviços
					list_services.remove(serv['name'])
				continue

			# verifica se o serviço está na lista para ser iniciado
			if serv['name'] not in list_services:
				# registro
				db.saveLog(['<<main:service:started>>', 'service', serv['name'], 'start', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
				list_services.append(serv['name']) # adiciona serviço na lista

				# verifica se o serviço está na lista de serviços parados
				if serv['name'] in list_service_stop:
					list_service_stop.remove(serv['name']) # remove serviço da lista
				
				# cria uma thread com um novo serviço
				thread.start_new_thread(Service, (db.getDataService(serv['name']),))

		time.sleep(abs(setting['time']))

if __name__ == '__main__':
	main()

