#-*- coding: utf-8 -*-

__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'

import json, os
from string import Template
from timeit import time

class Database:
	""" Serviço """
	def getDataServiceAll(self):
		data_services = []
		for (dir, nan, file) in os.walk('.'):
			if dir == './services':
				services = file
		for serv in services:
			name = os.path.join('services', serv)
			try:
				with open(name, 'r') as file:
					file_json = json.load(file)
					data_services.append(file_json)
			except Exception as erro:
				print('Erro ao abrir serviços:', erro)
				print('Tipo do erro:', type(erro))
		return data_services

	def getDataService(self, name):
		name_service = os.path.join('services', name)
		file_json = {}
		try:
			with open(name_service, 'r') as file:
				file_json = json.load(file)
				return file_json
		except FileNotFoundError:
			print('Serviço não encontrado!')
			return False
		except Exception as erro:
			print('Erro ao abrir serviço', erro)
			print('Tipo do erro:', type(erro))
			return False

	def saveService(self, data):
		name = os.path.join('services', data['name'])
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
		action = ''.join(['rm ', 'services/', name])
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

	# Logging
	def saveLog(self, data):
		new_data = '; '.join(data)
		try:
			with open('setting.log', 'a') as file:
				file.write(new_data+'\n')
		except Exception as erro:
			print('Tipo do erro: ', type(erro))


