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

	def getPidService(self):
		return str(os.getpid())

	def _checkDate(self, data):
		appointment = [[h, m, str(data['day']), str(data['month'])] for m in data['minute'] for h in data['hour']]
		current_time = ['0', '0', '0', '0']
		to_return = False
		for item in appointment:
			for i in range(4):
				if item[i] == '0':
					current_time[i] = '0'
				else:
					current_time[i] = str(int(self.date_list[i]))
			if item == current_time:
				to_return = True
				break
		return to_return

	def _checkRepeat(self, data, db, count):
		to_return = False
		if data['count'] > '-1':
			if str(count) == data['count']:
				data['state'] = 'stop' if data['mode'] == 'repeat' else 'wait'
				if data['state'] == 'wait': 
					db.saveLog(['<<service:waiting>>', data['name'], data['mode'], 'waiting', str(time.strftime('%d/%m/%Y-%H:%M:%S')), self.getPidService()])
				db.saveService(data)
				to_return = True
		return to_return

	def _notification(self, status, serv):
		if status == 'yes':
			notice = ' '.join(['notify-send -t 6000 -i /home/asfmint/mypy/schedule_tasks/img/logo_info.png', '"Schedule Tasks"', '"Serviço [ {} ] em execução."'.format(serv)])
			os.system(notice)
				
	def _main(self):
		db = Database()
		v_data = db.getDataService(self.data['name'])
		v_data['state'] = 'running' if (v_data['mode'] == 'date' and v_data['state'] == 'wait') or v_data['state'] == 'running' else 'stop'
		db.saveService(v_data)
		count = 0

		while True:
			serv = db.getDataService(self.data['name'])
			self.date_list = [i for i in time.strftime('%H %M %d %m').split()]
			if serv['state'] == 'stop':
				db.saveLog(['<<service:stopped>>', serv['name'], 'stop', str(time.strftime('%d/%m/%Y-%H:%M:%S')), self.getPidService()])
				break
			
			if serv['mode'] == 'repeat':
				self._notification(serv['notice'], serv['name'])
				os.system(serv['command'])
				count += 1
				db.saveLog(['<<service:executed>>', serv['name'], serv['mode'], 'running', str(serv['count']), str(serv['time']), str(time.strftime('%d/%m/%Y-%H:%M:%S')), self.getPidService()])
				if self._checkRepeat(serv, db, count): break
				time.sleep(MINUTE * abs(int(serv['time'])))

			elif serv['mode'] == 'date':
				if self._checkDate(serv):
					self._notification(serv['notice'], serv['name'])
					os.system(serv['command'])
					if int(serv['count']) > 0: count += 1
					db.saveLog(['<<service:executed>>', serv['name'], serv['mode'], serv['state'], str(serv['count']), str(time.strftime('%d/%m/%Y-%H:%M:%S')), self.getPidService()])
					if self._checkRepeat(serv, db, count): break
					time.sleep(MINUTE)
				else:
					time.sleep(MINUTE / 2)



