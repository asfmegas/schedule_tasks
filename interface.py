__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'
"""
Interface para gerênciar os arquivos

É através da Interface que são gerenciados os serviços criados. Com ela
é possível criar novos serviços, alterá-los ou removê-los, determinar 
suas duraçõesem tempo e quantidade de vezes executados e interromper um 
determinado serviço. Também é possível realizar alterações nas configura-
ções padrão.

"""

import os, json
import database
from constants import *

class Interface:
	def __init__(self):
		self.name = ''
		self.command = ''
		self.time = 0
		self.count = 0
		self.state = ''
		self.notice = ''
		self.deleteServ = ''
		self.mode = ''
		self.minute = 1
		self.hour = 1
		self.day = 1
		self.month = 1
		self.data = {}
		self.dataSetting = {}

	def options(self):
		print()
		print(' 1 - New service\n 2 - Change service\n 3 - Delete service\n 4 - List services\n 5 - Setting\n 6 - Sair')
		while True:
			print('-' * 30)
			option = Interface._getInt(' Option: ', 0)
			if option in ['1', '2', '3', '4', '5', '6']:
				break
			else:
				print(' Valor inválido!')
		print()
		return option

	def newService(self):
		os.system('clear')
		self.name = Interface._getString(' Name...: ', 0)
		self.command = Interface._getString(' Command: ', 0)
		self.notice = Interface._getString(' Notice.: ', 0)

		while True:
			self.state = Interface._getString(' State..: ', 0)
			if self.state in 'running stop'.split():
				break
			else:
				print('Valores possíveis: "running" ou "stop".')

		while True:
			self.mode = Interface._getString(' Mode...: ', 0)
			if self.mode in ['date', 'repeat']:
				if self.mode == 'date':
					self.minute = Interface._getIntDate(' Minute.: ', 'minute', 0)
					self.hour = Interface._getIntDate(' Hour...: ', 'hour', 0)
					self.day = Interface._getIntDate(' Day....: ', 'day', 0)
					self.month = Interface._getIntDate(' Month..: ', 'month', 0)
					self.time = "0"
					break
				else:
					self.minute = "0"
					self.hour = "0"
					self.day = "0"
					self.month = "0"
					self.time = Interface._getInt(' Time...: ', 0)
					break
			else:
				print('Opções válidas: "date" ou "repeat"')

		self.count = Interface._getInt(' Repeat.: ', 0)
		self.deleteServ = Interface._getString(' Delete.: ', 0)

	def save(self):
		self.data['name'] = self._normalizeText(self.name)
		self.data['command'] = self.command
		self.data['notice'] = self.notice # yes | no
		self.data['time'] = self.time # digit
		self.data['count'] = self.count # digit
		self.data['delete'] = self.deleteService # yes | no
		self.data['state'] = self.state # stop | running | (wait:only system)
		self.data['mode'] = self.mode # date | repeat
		self.data['minute'] = self.minute # 0-60
		self.data['hour'] = self.hour # 0-24
		self.data['day'] = self.day # 0-31
		self.data['month'] = self.month # 0-12

		db = database.Database()
		db.saveService(self.data)

	def updateService(self):
		db = database.Database()
		titles = self.getTitles()
		print('-' * 30)
		while True:
			name = self._normalizeText(Interface._getString(' Name: ', 0))
			if name in titles:
				break
			else:
				print('\n Esse serviço não existe!')
				print(titles)

		service = db.getDataService(name)
		os.system('clear')

		print()
		self.data['name'] = Interface._getString(' Name    ({}): '.format(service['name']), 1)
		if not self.data['name']:
			self.data['name'] = service['name']
		else:
			self.data['name'] = self._normalizeText(self.data['name'])

		self.data['command'] = Interface._getString(' Command ({}): '.format(service['command']), 1)
		if not self.data['command']:
			self.data['command'] = service['command']

		self.data['notice'] = Interface._getString(' Notice  ({}): '.format(service['notice']), 1)
		if not self.data['notice']:
			self.data['notice'] = service['notice']

		while True:
			self.data['state'] = Interface._getString(' State   ({}): '.format(service['state']), 1)
			if not self.data['state']:
				self.data['state'] = service['state']
				break
			if self.data['state'] in ['running', 'stop']:
				break
			else:
				print('Valores possíveis: "running" ou "stop".')

		while True:
			self.data['mode'] = Interface._getString(' Mode    ({}): '.format(service['mode']), 1)
			if not self.data['mode']:
				self.data['mode'] = service['mode']

			if self.data['mode'] in ['date', 'repeat']:
				if self.data['mode'] == 'date':

					self.data['minute'] = Interface._getIntDate(' Minute  ({}): '.format(service['minute']), 'minute', 1)
					if not self.data['minute'] and self.data['minute'] != 0:
						self.data['minute'] = service['minute']

					self.data['hour'] = Interface._getIntDate(' Hour    ({}): '.format(service['hour']), 'hour', 1)
					if not self.data['hour'] and self.data['hour'] != 0:
						self.data['hour'] = service['hour']

					self.data['day'] = Interface._getIntDate(' Day     ({}): '.format(service['day']), 'day', 1)
					if not self.data['day'] and self.data['day'] != 0:
						self.data['day'] = service['day']

					self.data['month'] = Interface._getIntDate(' Month   ({}): '.format(service['month']), 'month', 1)
					if not self.data['month'] and self.data['month'] != "0":
						self.data['month'] = service['month']

					self.data['time'] = "0"
					break
				else:
					self.data['minute'] = "0"
					self.data['hour'] = "0"
					self.data['day'] = "0"
					self.data['month'] = "0"

					self.data['time'] = Interface._getInt(' Time    ({}): '.format(service['time']), 1)
					if not self.data['time'] and self.data['time'] != "0":
						self.data['time'] = service['time']
					break
			else:
				print('Valores válidos: "date" ou "repeat"')

		self.data['count'] = Interface._getInt(' Repeat  ({}): '.format(service['count']), 1)
		if not self.data['count'] and self.data['count'] != '0':
			self.data['count'] = service['count']

		self.data['delete'] = Interface._getString(' Delete  ({}): '.format(service['delete']), 1)
		if not self.data['delete']:
			self.data['delete'] = service['delete']

		confirm = input(' Deseja salvar alterações? (yes|NO): ')
		if confirm.startswith('yes'):
			db.saveService(self.data)	

	def deleteService(self):
		db = database.Database()
		titles = self.getTitles()

		while True:
			name = self._normalizeText(Interface._getString(' Name: ', 0))
			if name in titles:
				break
			else:
				print('\n Esse serviço não existe!')
				print(titles)

		confirm = input(' Deseja apagar o serviço [ {} ]? (yes|NO): '.format(name))
		if confirm.startswith('yes'):
			db.deleteService(name)

	def getListService(self):
		db = database.Database()
		setting = db.getDataSetting()
		os.system('clear')
		print('\n\tLista de serviços criados:')
		print()
		print(' No  Name                State   Time Repeat Notice Mode    Appointment   Command')
		print('-----------------------------------------------------------------------------------------------')
		count = 1
		for item in db.getDataServiceAll():
			app = str(item['hour'])+':'+str(item['minute'])+'-'+str(item['day'])+'/'+str(item['month'])
			print(' {cnt:2}. {name:19} {state:7} {tm:6} {repeat:4} {notice:6} {mode:8} {appoint:12} {cmd}'.format(cnt=count,
																										name=item['name'],
																										state=item['state'],
																										tm=str(item['time']),
																										repeat=str(item['count']),
																										notice=item['notice'],
																										mode=item['mode'],
																										appoint=app,
																										cmd=item['command']))
			count += 1
		print('-----------------------------------------------------------------------------------------------')
		print('\tSetting: time({}) state({})'.format(setting['time'], setting['state']))

	def getTitles(self):
		db = database.Database()
		titles = []
		for service in db.getDataServiceAll():
			titles.append(service['name'])
		return titles

	def _getString(label, flag):
		to_return = ''
		while True:
			to_return = input(label)
			if to_return: break
			if not to_return and flag == 1: break
			else:
				print(' Digite o "{}"'.format(label))
		return to_return

	def _getInt(label, flag):
		number = 0
		while True:
			number = input(label)
			if not number and flag == 1:
				break
			if number.isdigit() or number == '-1':
				break
			else:
				print(' Valor incorreto!')
		return number

	def _getIntDate(label, attr, flag):
		number = ''
		list_number = []
		count = 0
		while True:
			number = input(label)
			if not number and flag == 1:
				if Interface._checkValidity(attr, '0'):
					break

			if not Interface._checkValidity(attr, number):
				print('Valor incorreto! ({})'.format(number))
				continue

			for value in number.split(','):
				if attr == 'day' or attr == 'month':
					return value
				else:
					list_number.append(value)
			break
		return list_number

	def _checkValidity(attr, enter):
		if attr == 'hour': value = HOUR
		elif attr == 'minute': value = MINUTE
		elif attr == 'day': value = DAY
		else: value = MONTH
		options = [str(i) for i in range(0, value + 1)]
		for value in enter.split(','):
			if value not in options:
				return False
		return True

	def _normalizeText(self, text):
		new_text = []
		for i in list(text):
			if i != '\n':
				if i == ' ':
					new_text.append('_')
				else:
					new_text.append(i)
		text = ''.join(new_text)
		return text

	def setting(self):
		db = database.Database()
		data = db.getDataSetting()
		os.system('clear')
		while True:
			self.dataSetting['time'] = input('Time ({}): '.format(data['time']))
			if not self.dataSetting['time']:
				self.dataSetting['time'] = data['time']
				break
			else:
				try:
					self.dataSetting['time'] = int(self.dataSetting['time'])
					break
				except:
					print(' Digite um valor inteiro.')

		self.dataSetting['state'] = input('State ({}): '.format(data['state']))
		if not self.dataSetting['state']:
			self.dataSetting['state'] = data['state']

		db.updateSetting(self.dataSetting)
