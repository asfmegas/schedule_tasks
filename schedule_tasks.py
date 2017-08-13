#-*- coding: utf-8 -*-

from tkinter import *
import tkinter

from database import Database

FUNDO_PRINCIPAL = '#201d1d'
FONTE_PADRAO_LABEL = ('arial', 18, 'bold')
FONTE_PADRAO_CONTEUDO = ('arial', 18)

class ClasseBotoes(Button):
	def __init__(self, parent=None, nome='', cmd=None):
		super(ClasseBotoes, self).__init__(parent)
		self.config(text=nome, command=cmd, font=FONTE_PADRAO_LABEL, cursor='hand2')

class ClasseLabel(Label):
	def __init__(self, parent=None, texto='', w=8):
		super(ClasseLabel, self).__init__(parent)
		self.pack(side=LEFT)
		self.config(text=texto, 
					width=w,
					font=FONTE_PADRAO_LABEL,
					anchor=W)

class ClasseEntry(Entry):
	def __init__(self, parent=None, w=6, j=LEFT, var=None):
		super(ClasseEntry, self).__init__(parent)
		self.config(font=FONTE_PADRAO_CONTEUDO,
					width=w,
					justify=j,
					bg="black",
					fg="white",
					textvariable=var)

class ClasseRadiobutton(Radiobutton):
	def __init__(self, parent=None, texto='', valor='', var='', cmd=None):
		super(ClasseRadiobutton, self).__init__(parent)
		self.config(text=texto, variable=var,
								command=cmd,
								value=valor,
								# textvariable='yes',
								bg="#cccccc", # cor de fundo
								fg="black", # cor de texto
								font=FONTE_PADRAO_LABEL,
								wraplength=0, # orientação 0 - horizontal; 1 - vertical
								width=8, # largura
								height=1, # altura
								relief=SOLID, # tipo de borda
								cursor='hand2', # icone do mouse
								borderwidth=5, # espessura da borda
								highlightcolor="red", # quando selecionado cia tab
								# highlightbackground="blue", # cor da borda externa
								activeforeground="black",  # cor do texto quando o mouse se posiciona em cima
								activebackground="grey", # cor quando mouse se posiciona em cima
								selectcolor="grey", # cor de dentro do círculo
								# padx=2, 
								# pady=2,
								anchor=CENTER) # centralizar texto

class ClasseToplevelPrincipal(Toplevel):
	def __init__(self, titulo='', dados=None, value=0):
		super(ClasseToplevelPrincipal, self).__init__()
		self.title(titulo)
		self.config(padx=10, pady=10)

		self.dados = dados
		self.value = value

		self.nome_entrada = self.nome()
		self.notice_entrada = self.notice()
		self.delete_entrada = self.deleteService()
		self.state_entrada = self.state()
		self.mode_entrada = self.mode()
		self.repeat_entrada = self.repeat()

		self.time_entrada = self.time()

		self.minute_entrada = self.minute()
		self.hour_entrada = self.hour()
		self.day_entrada = self.day()
		self.month_entrada = self.month()

		self.comando_entrada = self.comando()
		self.botoes()

		self.definirModo()

		self.geometry("900x600")

		""" modal """
		self.focus_set()
		self.grab_set()
		self.wait_window()

	def definirModo(self):
		if self.value == 1:
			if self.dados['mode'] == 'date':
				self.controleDate()
			else:
				self.controleRepeat()

	def nome(self):
		frame = Frame(self)
		frame.pack(side=TOP, expand=YES, fill=X)

		ClasseLabel(frame, texto="Nome: ")

		var = StringVar()
		entrada = ClasseEntry(frame, var=var)
		entrada.pack(side=LEFT, expand=YES, fill=X)
		if self.value == 1:
			var.set(self.dados['name'])
		entrada.focus()

		return entrada

	def lista(self):
		frame = Frame(self, bg="blue")
		frame.pack(side=TOP, expand=YES, fill=X)

		ClasseLabel(frame, texto="Command: ")

		scrollbar = Scrollbar(frame)

		entrada = Listbox(frame, relief=SUNKEN, font=FONTE_PADRAO)
		entrada.pack(side=LEFT, expand=YES, fill=X)
		entrada.config(yscrollcommand=scrollbar.set, selectmode=EXTENDED)

		scrollbar.config(command=entrada.yview)
		scrollbar.pack(side=RIGHT, fill=X)

		entrada.insert(0, 'comando 1')

	def comando(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Command: ", w=10)

		frame_text = Frame(frame)
		frame_text.pack(side=RIGHT, expand=YES, fill=X)

		entrada = Text(frame_text, font=FONTE_PADRAO_CONTEUDO, 
									padx=4,
									pady=2,
									height=2, 
									bg="black", 
									fg="white")
		entrada.pack(side=LEFT, expand=YES, fill=X)
		entrada.mark_set(INSERT, '1.0')
		if self.value == 1:
			entrada.insert('1.0', self.dados['command'])

		return entrada

	def notice(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Notice: ")

		var = StringVar()
		notice_yes = ClasseRadiobutton(frame, texto="Yes", valor="yes", var=var).pack(side=LEFT)
		notice_no = ClasseRadiobutton(frame, texto="No", valor="no", var=var).pack(side=LEFT)

		# definir valor
		if self.value == 1:
			if self.dados['notice'] == 'yes':
				var.set('yes')
			else:
				var.set('no')

		return var

	def state(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="State: ")

		var = StringVar()
		state_running = ClasseRadiobutton(frame, texto="Running", valor="running", var=var).pack(side=LEFT)
		state_stop = ClasseRadiobutton(frame, texto="Stop", valor="stop", var=var).pack(side=LEFT)

		if self.value == 1:
			if self.dados['state'] == 'running':
				var.set('running')
			else:
				var.set('stop')

		return var

	def mode(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Mode: ")

		var = StringVar()
		repeat = ClasseRadiobutton(frame, texto="Repeat", valor="repeat", var=var, cmd=self.controleRepeat)
		repeat.pack(side=LEFT)

		date = ClasseRadiobutton(frame, texto="Date", valor="date", var=var, cmd=self.controleDate)
		date.pack(side=LEFT)

		if self.value == 1:
			if self.dados['mode'] == 'repeat':
				var.set('repeat')
			else:
				var.set('date')

		return var

	def repeat(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Repeat: ")

		var = StringVar()
		entrada = ClasseEntry(frame, w=6, j=CENTER, var=var)
		entrada.pack(side=LEFT)
		if self.value == 1:
			var.set(self.dados['count'])

		return entrada

	def time(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Time: ")

		var = StringVar()
		entrada = ClasseEntry(frame, w=6, j=CENTER, var=var)
		entrada.pack(side=LEFT)
		if self.value == 1:
			var.set(self.dados['time'])

		return entrada

	def minute(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Minute: ")

		var = StringVar()
		entrada = Entry(frame, font=FONTE_PADRAO_CONTEUDO, textvariable=var)
		entrada.pack(side=LEFT)
		entrada.config(width=12, justify=CENTER, state=DISABLED, bg="black", fg="white")
		if self.value == 1:
			var.set(','.join(self.dados['minute']))

		return entrada

	def hour(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Hour: ")

		var = StringVar()
		entrada = Entry(frame, font=FONTE_PADRAO_CONTEUDO, textvariable=var)
		entrada.pack(side=LEFT)
		entrada.config(width=12, justify=CENTER, state=DISABLED, bg="black", fg="white")
		if self.value == 1:
			var.set(','.join(self.dados['hour']))

		return entrada

	def day(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Day: ")

		var = IntVar()
		scale = Scale(frame, variable=var, from_=0,  
											to=31,
											bg=FUNDO_PRINCIPAL,
											fg="white",
											showvalue=YES, 
											resolution=1, 
											tickinterval=1, 
											orient=HORIZONTAL)
		scale.pack(side=LEFT, expand=YES, fill=X)
		if self.value == 1:
			var.set(int(self.dados['day']))

		return var

	def month(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Month: ")

		var = IntVar()
		scale = Scale(frame, variable=var, 
									from_=0, 
									to=12,
									bg=FUNDO_PRINCIPAL,
									fg="white",  
									showvalue=YES, 
									resolution=1, 
									tickinterval=1, 
									orient=HORIZONTAL)
		scale.pack(side=LEFT, expand=YES, fill=X)
		if self.value == 1:
			var.set(int(self.dados['month']))

		return var

	def deleteService(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Delete: ")

		var = StringVar()
		ClasseRadiobutton(frame, texto="Yes", valor="yes", var=var).pack(side=LEFT)
		ClasseRadiobutton(frame, texto="No", valor="no", var=var).pack(side=LEFT)
		if self.value == 1:
			var.set(self.dados['delete'])

		return var

	def salvarDados(self):
		db = Database()
		count = 0
		if self.verificarDados(self.nome_entrada.get()):
			self.dados['name'] = self._normalizeText(self.nome_entrada.get())
			print('name')
			count += 1

		if self.verificarDados(self.notice_entrada.get()):
			self.dados['notice'] = self.notice_entrada.get()
			print('notice')
			count += 1

		if self.verificarDados(self.delete_entrada.get()):
			self.dados['delete'] = self.delete_entrada.get()
			print('delete')
			count += 1

		if self.verificarDados(self.state_entrada.get()):
			self.dados['state'] = self.state_entrada.get()
			print('state')
			count += 1

		if self.verificarDados(self.mode_entrada.get()):	
			self.dados['mode'] = self.mode_entrada.get()
			print('mode')
			count += 1

		if self.verificarDados(self.repeat_entrada.get()):
			self.dados['count'] = self.repeat_entrada.get()
			print('count')
			count += 1

		if self.verificarDados(self.comando_entrada.get('1.0', END+'-1c')):
			self.dados['command'] = self.comando_entrada.get('1.0', END+'-1c')
			print('command')
			count += 1

		if self.dados['mode'] == 'date':
			if self.verificarDados(self.minute_entrada.get()):
				self.dados['minute'] = self.minute_entrada.get().split(',')
				print('minute')
				count += 1

			if self.verificarDados(self.hour_entrada.get()):
				self.dados['hour'] = self.hour_entrada.get().split(',')
				print('hour')
				count += 1

			if self.verificarDados(self.day_entrada.get()):
				self.dados['day'] = self.day_entrada.get()
				print('day')
				count += 1
			else:
				print('else: day')
				self.dados['day'] = '0'
				count += 1

			if self.verificarDados(self.month_entrada.get()):
				self.dados['month'] = self.month_entrada.get()
				print('month')
				count += 1
			else:
				print('else: month')
				self.dados['month'] = '0'
				count += 1

			self.dados['time'] = '0'
			print('time')
			count += 1
		else:
			if self.verificarDados(self.time_entrada.get()):
				self.dados['time'] = self.time_entrada.get()
				print('time')
				count += 1

			self.dados['minute'] = '0'
			print('minute')
			count += 1
			self.dados['hour'] = '0'
			print('hour')
			count += 1
			self.dados['day'] = '0'
			print('day')
			count += 1
			self.dados['month'] = '0'
			print('month')
			count += 1

		print('count: ', count)
		if count == 12:
			print(self.dados)
			db.saveService(self.dados)
			self.destroy()
		else:
			print('Não pode haver campos em branco.')

		# print('Nome:', self.nome_entrada.get())
		# print('Notice:', self.notice_entrada.get())
		# print('Delete:', self.delete_entrada.get())
		# print('State:', self.state_entrada.get())
		# print('Mode:', self.mode_entrada.get())
		# print('Repeat:', self.repeat_entrada.get())

		# if self.dados['mode'] == 'date':
		# 	print('Minute:', self.minute_entrada.get())
		# 	print('Hour:', self.hour_entrada.get())
		# 	print('Day:', self.day_entrada.get())
		# 	print('Month:', self.month_entrada.get())
		# else:
		# 	print('Time:', self.time_entrada.get())

		# print('Comando:', self.comando_entrada.get('1.0', END+'-1c'))

	def controleRepeat(self):
		self.time_entrada.config(state=NORMAL)

		self.minute_entrada.config(state=DISABLED)
		self.hour_entrada.config(state=DISABLED)

	def controleDate(self):
		self.time_entrada.config(state=DISABLED)

		self.minute_entrada.config(state=NORMAL)
		self.hour_entrada.config(state=NORMAL)

	def botoes(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)
		frame.config(bd=2, relief=GROOVE, padx=5, pady=5)

		ClasseBotoes(frame, 'Fechar', cmd=self.destroy).pack(side=RIGHT)
		ClasseBotoes(frame, 'Salvar', cmd=self.salvarDados).pack(side=RIGHT)

	def verificarDados(self, value):
		if value:
			return True
		return False

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
		
class ClassToplevelDelete(Toplevel):
	pass

class ClasseFrame(Frame):
	def __init__(self, parent=None, acao='update'):
		super(ClasseFrame, self).__init__(parent)
		self.config(bg="#cccccc", padx=2, pady=2)
		self.pack(fill=BOTH, expand=YES)
		self.lista()

		self.acao = acao

	def lista(self):
		db = Database()

		opcoes = [service['name'] for service in db.getDataServiceAll()]
		scrollbar = Scrollbar(self)

		lista_service = Listbox(self, relief=SUNKEN, font=FONTE_PADRAO_CONTEUDO)
		scrollbar.config(command=lista_service.yview)
		lista_service.config(yscrollcommand=scrollbar.set)
		scrollbar.pack(side=RIGHT, fill=Y)
		lista_service.pack(side=LEFT, expand=YES, fill=BOTH)
		
		pos = 0
		for label in opcoes:
			lista_service.insert(pos, label)
			pos += 1

		lista_service.bind('<Double-1>', lambda eventos: self.definirAcao(lista_service.get(lista_service.curselection())))

	def definirAcao(self, service):
		if self.acao == 'update':
			self.updateService(service)
		else:
			self.deleteService(service)

	def updateService(self, service):
		db = Database()
		dados = db.getDataService(service)
		ClasseToplevelPrincipal('Alterar Serviço', dados, value=1)

	def deleteService(self, service):
		db = Database()
		db.deleteService(service)
		# print(service)


class ClassToplevelList(Toplevel):
	def __init__(self, acao='update', titulo=''):
		super(ClassToplevelList, self).__init__()
		self.title(titulo)

		self.labelTitulo(titulo)
		ClasseFrame(self, acao)
		self.geometry("300x500")

		self.botoes()

		self.focus_set()
		self.grab_set()
		self.wait_window()
		self.mainloop()

	def labelTitulo(self, titulo):
		Label(self, text=titulo, font=FONTE_PADRAO_LABEL).pack(fill=X, expand=YES)

	def botoes(self):
		frame = Frame(self)
		frame.pack()

		ClasseBotoes(self, nome="Fechar", cmd=self.destroy).pack(side=RIGHT, fill=X, expand=YES)

class ClasseLabelPrincipal(Frame):
	def __init__(self, parent=None):
		super(ClasseLabelPrincipal, self).__init__(parent)
		self.pack(expand=YES, fill=BOTH)
		self.config(bg=FUNDO_PRINCIPAL)
		self.lista = {
				"novo": self.newService,
				"alterar": self.updateService,
				"apagar": self.deleteService,
				"listar": self.listService,
				"sair": quit
			}
		self.botoes()

	def botoes(self):
		ClasseBotoes(self, 'Novo', cmd=self.lista['novo']).pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Alterar', cmd=self.lista['alterar']).pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Apagar', cmd=self.lista['apagar']).pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Listar').pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Sair', cmd=self.lista['sair']).pack(expand=YES, fill=BOTH)

	def newService(self):
		dados = {"name": "", "notice": "", "command": "", "hour": "", "time": "", "count": "", "month": "0", "day": "0", "minute": "", "state": "", "delete": "", "mode": ""}
		ClasseToplevelPrincipal('Criar Novo Serviço', dados)

	def updateService(self):
		ClassToplevelList(titulo='Atualizar Serviços')
		# dados = { "name": "gal_img_2", "notice": "yes", "command": "gal -m jpeg", "hour": ["22"], "time": "0", "count": "-1", "month": "10", "day": "20", "minute": ["30"], "state": "running", "delete": "no", "mode": "date" }
		# ClasseToplevelPrincipal('Alterar Serviço', dados, value=1)

	def deleteService(self):
		ClassToplevelList(acao='delete', titulo="Apagar Serviços")

	def listService(self):
		pass

if __name__ == '__main__':
	janela_principal = Tk()
	janela_principal.title("Schedule Tasks")

	frame1 = ClasseLabelPrincipal(janela_principal)

	janela_principal.geometry("250x350")
	janela_principal.mainloop()


