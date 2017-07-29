__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'

import os

from interface import Interface

os.chdir('/home/asfmint/mypy/schedule_tasks')

while True:
	i = Interface()
	option = i.options()
	if option == 1:
		i.newService()
		i.save()
	elif option == 2:
		count = 1
		print('\n Comandos:')
		for title in i.getTitles():
			print(' {}. {}'.format(count, title))
			count += 1
		print()
		i.updateService()
		i.save()
	elif option == 3:
		i.deleteService()
	elif option == 4:
		i.getListService()
	elif option == 5:
		i.setting()
	elif option == 6:
		break