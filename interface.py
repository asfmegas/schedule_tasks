__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'

import os, json
import database

class Interface:
	def __init__(self):
		self.name = ''
		self.command = ''
		self.time = 0
		self.count = 0
		self.state = ''
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
				print('Valor inválido!')
		print()
		return option

	def newService(self):
		self.name = Interface._getString('Name...: ')
		self.command = Interface._getString('Command: ')
		self.time = Interface._getInt('Time...: ')
		self.count = Interface._getInt('Repeat.: ')
		self.state = Interface._getString('State..: ')

	def save(self):
		self.data['name'] = self.name
		self.data['command'] = self.command
		self.data['time'] = self.time
		self.data['count'] = self.count
		self.data['state'] = self.state # stop | running
		db = database.Database()
		db.saveService(self.data)

	def updateService(self):
		db = database.Database()
		titles = []
		for item in db.getDataServiceAll():
			titles.append(item['name'])

		while True:
			name = Interface._getString(' Name: ')
			if name in titles:
				break
			else:
				print('\nEsse comando não existe!')
				print(titles)

		service = db.getDataService(name)
		os.system('clear')

		print()
		self.data['name'] = input(' Name ({}): '.format(service['name']))
		if not self.data['name']:
			self.data['name'] = service['name']

		self.data['command'] = input(' Command ({}): '.format(service['command']))
		if not self.data['command']:
			self.data['command'] = service['command']

		self.data['time'] = input(' Time ({}): '.format(service['time']))
		if not self.data['time']:
			self.data['time'] = service['time']

		self.data['count'] = input(' Repeat ({}): '.format(service['count']))
		if not self.data['count']:
			self.data['count'] = service['count']

		self.data['state'] = input(' State ({}): '.format(service['state']))
		if not self.data['state']:
			self.data['state'] = service['state']

		db.saveService(self.data)

	def deleteService(self):
		db = database.Database()
		name = Interface._getString('Name: ')
		db.deleteService(name)

	def getListService(self):
		db = database.Database()
		os.system('clear')
		print('\n\tLista de comandos criados:')
		print()
		count = 1
		for item in db.getDataServiceAll():
			print(' {}. Name: {}; State: {}; Time: {}; Loop: {}'.format(count, item['name'], item['state'], item['time'], item['count']))
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
				print('Digite o "{}"'.format(label))
		return to_return

	def _getInt(label):
		number = 0
		while True:
			try:
				number = int(input(label))
			except:
				print('Valor incorreto!')
			else:
				break
		return number

	def setting(self):
		db = database.Database()
		data = db.getDataSetting()

		self.dataSetting['time'] = input('Time ({}): '.format(data['time']))
		if not self.dataSetting['time']:
			self.dataSetting['time'] = data['time']

		self.dataSetting['state'] = input('State ({}): '.format(data['state']))
		if not self.dataSetting['state']:
			self.dataSetting['state'] = data['state']

		db.updateSetting(self.dataSetting)
