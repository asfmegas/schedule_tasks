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

class Interface:
	def __init__(self):
		self.name = ''
		self.command = ''
		self.time = 0
		self.count = 0
		self.state = ''
		self.notice = ''
		self.data = {}
		self.dataSetting = {}

	def options(self):
		print()
		print(' 1 - New service\n 2 - Change service\n 3 - Delete service\n 4 - List services\n 5 - Setting\n 6 - Sair')
		while True:
			option = Interface._getInt(' Option: ')
			if option in [1, 2, 3, 4, 5, 6]:
				break
			else:
				print(' Valor inválido!')
		print()
		return option

	def newService(self):
		self.name = Interface._getString('Name...: ')
		self.command = Interface._getString('Command: ')
		self.notice = Interface._getString('Notice.: ')
		self.time = Interface._getInt('Time...: ')
		self.count = Interface._getInt('Repeat.: ')
		self.state = Interface._getString('State..: ')

	def save(self):
		self.data['name'] = self._normalizeText(self.name)
		self.data['command'] = self.command
		self.data['notice'] = self.notice # yes | no
		self.data['time'] = self.time
		self.data['count'] = self.count
		self.data['state'] = self.state # stop | running
		db = database.Database()
		db.saveService(self.data)

	def updateService(self):
		db = database.Database()
		titles = self.getTitles()

		while True:
			name = self._normalizeText(Interface._getString(' Name: '))
			if name in titles:
				break
			else:
				print('\n Esse comando não existe!')
				print(titles)

		service = db.getDataService(name)
		os.system('clear')

		print()
		self.data['name'] = input(' Name ({}): '.format(service['name']))
		if not self.data['name']:
			self.data['name'] = service['name']
		else:
			self.data['name'] = self._normalizeText(self.data['name'])

		self.data['command'] = input(' Command ({}): '.format(service['command']))
		if not self.data['command']:
			self.data['command'] = service['command']

		self.data['notice'] = input(' Notice ({}): '.format(service['notice']))
		if not self.data['notice']:
			self.data['notice'] = service['notice']

		while True:
			self.data['time'] = input(' Time ({}): '.format(service['time']))
			if not self.data['time']:
				self.data['time'] = service['time']
				break
			else:
				try:
					self.data['time'] = int(self.data['time'])
					break
				except:
					print(' Digite apenas números inteiros')

		while True:
			self.data['count'] = input(' Repeat ({}): '.format(service['count']))
			if not self.data['count']:
				self.data['count'] = service['count']
				break
			else:
				try:
					self.data['count'] = int(self.data['count'])
					break
				except:
					print(' Digite apenas números inteitos!')

		self.data['state'] = input(' State ({}): '.format(service['state']))
		if not self.data['state']:
			self.data['state'] = service['state']

		db.saveService(self.data)

	def deleteService(self):
		db = database.Database()
		titles = self.getTitles()

		while True:
			name = self._normalizeText(Interface._getString(' Name: '))
			if name in titles:
				break
			else:
				print('\n Esse comando não existe!')
				print(titles)

		db.deleteService(name)

	def getListService(self):
		db = database.Database()
		os.system('clear')
		print('\n\tLista de comandos criados:')
		print()
		count = 1
		for item in db.getDataServiceAll():
			print(' {}. Name: {}; State: {}; Time: {}; Loop: {}; Notice: {}'.format(count, item['name'], item['state'], item['time'], item['count'], item['notice']))
			print('    Command: {}'.format(item['command']))
			print()
			count += 1

	def getTitles(self):
		db = database.Database()
		titles = []
		for service in db.getDataServiceAll():
			titles.append(service['name'])
		return titles

	def _getString(label):
		to_return = ''
		while True:
			to_return = input(label)
			if to_return:
				break
			else:
				print(' Digite o "{}"'.format(label))
		return to_return

	def _getInt(label):
		number = 0
		while True:
			try:
				number = int(input(label))
			except:
				print(' Valor incorreto!')
			else:
				break
		return number

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
