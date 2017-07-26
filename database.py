__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'

import json, os
from string import Template

class Database:
	# Serviço
	def getDataServiceAll(self):
		data_services = []
		for (dir, nan, file) in os.walk('.'):
			if dir == './services':
				services = file
		for serv in services:
			name = 'services/{}'.format(serv)
			try:
				with open(name, 'r') as file:
					file_json = json.load(file)
					data_services.append(file_json)
			except Exception as erro:
				print('Erro ao abrir serviços:', erro)
				print('Tipo do erro:', type(erro))
		return data_services

	def getDataService(self, name):
		name_service = 'services/{}'.format(name)
		file_json = {}
		try:
			with open(name_service, 'r') as file:
				file_json = json.load(file)
				return file_json
		except FileNotFoundError:
			print("Serviço não encontrado!")
			return False
		except Exception as erro:
			print('Erro ao abrir serviço', erro)
			print('Tipo do erro:', type(erro))
			return False

	def saveService(self, data):
		name = 'services/{}'.format(data['name'])
		file_json = json.dumps(data, indent=2, sort_keys=False)
		try:
			with open(name, 'w') as file:
				file.write(file_json)
		except IsADirectoryError:
			pass
		except Exception as erro:
			print('Erro ao criar serviço:', erro)
			print('Tipo do erro:', type(erro))

	def deleteService(self, name):
		action = 'rm services/{}'.format(name)
		os.system(action)

	# Config
	# Retorna um dicionário com os dados de config
	def getDataSetting(self):
		try:
			with open('config.json', 'r') as file:
				file_json = json.load(file)
		except Exception as erro:
			print('Erro ao abrir config:', erro)
			print('Tipo do erro:', type(erro))
		return file_json

	# Recebe um dicionário com os dados de config
	def updateSetting(self, data):
		file_json = json.dumps(data, indent=4, sort_keys=False)
		try:
			with open('config.json', 'w') as file:
				file.write(file_json)
		except Exception as erro:
			print('Erro ao salvar config:', erro)
			print('Tipo do erro:', type(erro))


