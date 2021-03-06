__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'

import os

from interface import Interface

os.chdir('/home/asfmint/mypy/schedule_tasks')

while True:
	i = Interface()
	option = i.options()
	if option == '1':
		i.newService()
		i.save()
	elif option == '2':
		count = 1
		print('\n Lista de serviços:')
		for title in i.getTitles():
			print(' {:3}. {}'.format(count, title))
			count += 1
		print()
		i.updateService()
		i.save()
	elif option == '3':
		i.deleteService()
	elif option == '4':
		i.getListService()
	elif option == '5':
		i.setting()
	elif option in '6 exit quit sair'.split():
		print(' Bye!!!')
		break