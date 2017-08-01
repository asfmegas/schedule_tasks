__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'

import os
from timeit import time

from database import Database
from constants import *

os.chdir('/home/asfmint/mypy/schedule_tasks')

class Service:
	def __init__(self, data):
		self.data = data
		self._main()
		self.date_list = []

	def _checkDate(self, data):
		appointment = [data['hour'], data['minute'], data['day'], data['month']]
		current_time = [(0 if appointment[i] == 0 else self.date_list[i]) for i in range(4)]
		return current_time == appointment

	def _checkRepeat(self, data, db, count):
		to_return = False
		if data['count'] > -1:
			if count == data['count']:
				data['state'] = 'stop' if data['mode'] == 'repeat' else 'wait'
				if data['state'] == 'wait': 
					db.saveLog(['<<service:waiting>>', serv['name'], 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
				db.saveService(data)
				to_return = True
		return to_return
				
	def _main(self):
		db = Database()
		v_data = db.getDataService(self.data['name'])
		v_data['state'] = 'running' if (v_data['mode'] == 'date' and v_data['state'] == 'wait') or v_data['state'] == 'running' else 'stop'
		db.saveService(v_data)
		count = 0
		while True:
			serv = db.getDataService(self.data['name'])
			self.date_list = [int(i) for i in time.strftime('%H %M %d %m').split()]
			if serv['state'] == 'stop':
				db.saveLog(['<<service:stopped>>', serv['name'], 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
				break
			
			if serv['mode'] == 'repeat':
				if serv['notice'] == 'yes':
					notice = ' '.join(['notify-send -t 6000 -i /home/asfmint/mypy/schedule_tasks/img/logo_info.png', '"Schedule Tasks"', '"Serviço [ {} ] em execução."'.format(serv['name'])])
					os.system(notice)
				os.system(serv['command'])
				count += 1
				db.saveLog(['<<service:running>>', serv['name'], serv['mode'], 'running', str(serv['count']), str(serv['time']), str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
				if self._checkRepeat(serv, db, count): break
				time.sleep(MINUTE * abs(serv['time']))

			elif serv['mode'] == 'date':
				if self._checkDate(serv):
					if serv['notice'] == 'yes':
						notice = ' '.join(['notify-send -t 6000 -i /home/asfmint/mypy/schedule_tasks/img/logo_info.png', '"Schedule Tasks"', '"Serviço [ {} ] em execução."'.format(serv['name'])])
						os.system(notice)
					os.system(serv['command'])
					if serv['count'] > 0: count += 1
					db.saveLog(['<<service:running>>', serv['name'], serv['mode'], 'running', str(serv['count']), str(time.strftime('%d/%m/%Y-%H:%M:%S'))])
					if self._checkRepeat(serv, db, count): break
					time.sleep(MINUTE)
				else:
					time.sleep(30)



