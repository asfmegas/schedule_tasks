#-*- coding: utf-8 -*-

from tkinter import *
import tkinter, os
from tkinter.messagebox import *

os.chdir('/home/asfmint/mypy/schedule_tasks')

from database import Database
from constants import *

class ClasseBotoes(Button):
	def __init__(self, parent=None, nome='', cmd=None):
		super(ClasseBotoes, self).__init__(parent)
		self.config(text=nome, command=cmd, 
								font=FONTE_PADRAO_LABEL, 
								cursor='hand2', 
								bd=6,
								width=10,
								relief=GROOVE)

class ClasseLabel(Label):
	def __init__(self, parent=None, texto='', w=8, s=LEFT):
		super(ClasseLabel, self).__init__(parent)
		self.pack(side=s)
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
					bg="#cccccc",
					fg="black",
					textvariable=var)

class ClasseRadiobutton(Radiobutton):
	def __init__(self, parent=None, texto='', valor='', var='', cmd=None):
		super(ClasseRadiobutton, self).__init__(parent)
		self.config(text=texto, variable=var,
								command=cmd,
								value=valor,
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
								highlightbackground="grey", # cor da borda externa
								activeforeground="black",  # cor do texto quando o mouse se posiciona em cima
								activebackground="grey", # cor quando mouse se posiciona em cima
								selectcolor="white", # cor de dentro do círculo
								anchor=W) # centralizar texto

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

	def formatarCamposData(self, var):
		texto = ''
		for i in list(var.get()):
			if str(i).isdigit() or str(i) == ',':
				texto += i
		var.set(texto)

	def formatarCampos(self, var):
		texto = ''
		for i in list(var.get()):
			if str(i).isdigit() or str(i) == '-':
				texto += i
		var.set(texto)

	def nome(self):
		frame = Frame(self)
		frame.pack(side=TOP, expand=YES, fill=X)

		ClasseLabel(frame, texto="Name: ")

		var = StringVar()
		entrada = ClasseEntry(frame, var=var)
		entrada.pack(side=LEFT, expand=YES, fill=X)
		if self.value == 1:
			var.set(self.dados['name'])
		entrada.focus()

		return entrada

	def lista(self):
		frame = Frame(self)
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
									bg="#cccccc", 
									fg="black")
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

		var.trace_variable("w", lambda x, y, z: self.formatarCampos(var))
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

		var.trace_variable("w", lambda x, y, z: self.formatarCampos(var))
		return entrada

	def minute(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Minute: ")

		var = StringVar()
		entrada = Entry(frame, font=FONTE_PADRAO_CONTEUDO, textvariable=var)
		entrada.pack(side=LEFT)
		entrada.config(width=12, justify=CENTER, state=DISABLED, bg="#cccccc", fg="black")
		if self.value == 1:
			var.set(','.join(self.dados['minute']))

		var.trace_variable("w", lambda x, y, z: self.formatarCamposData(var))
		ClasseLabel(frame, texto=" ex.: 12,13,14", w=15)

		return entrada

	def hour(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		ClasseLabel(frame, texto="Hour: ")

		var = StringVar()
		entrada = Entry(frame, font=FONTE_PADRAO_CONTEUDO, textvariable=var)
		entrada.pack(side=LEFT)
		entrada.config(width=12, justify=CENTER, state=DISABLED, bg="#cccccc", fg="black")
		if self.value == 1:
			var.set(','.join(self.dados['hour']))

		var.trace_variable("w", lambda x, y, z: self.formatarCamposData(var))
		ClasseLabel(frame, texto=" ex.: 14,18,20", w=15)

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
											cursor='hand2',
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
									cursor='hand2',
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
			self.dados['name'] = self._normalizeText(self.nome_entrada.get()[:16])
			count += 1

		if self.verificarDados(self.notice_entrada.get()):
			self.dados['notice'] = self.notice_entrada.get()
			count += 1

		if self.verificarDados(self.delete_entrada.get()):
			self.dados['delete'] = self.delete_entrada.get()
			count += 1

		if self.verificarDados(self.state_entrada.get()):
			self.dados['state'] = self.state_entrada.get()
			count += 1

		if self.verificarDados(self.mode_entrada.get()):	
			self.dados['mode'] = self.mode_entrada.get()
			count += 1

		if self.verificarDados(self.repeat_entrada.get()):
			self.dados['count'] = self.repeat_entrada.get()
			count += 1

		if self.verificarDados(self.comando_entrada.get('1.0', END+'-1c')):
			self.dados['command'] = self.comando_entrada.get('1.0', END+'-1c')
			count += 1

		if self.dados['mode'] == 'date':
			if self.verificarDados(self.minute_entrada.get()):
				self.dados['minute'] = self.minute_entrada.get().split(',')
				count += 1

			if self.verificarDados(self.hour_entrada.get()):
				self.dados['hour'] = self.hour_entrada.get().split(',')
				count += 1

			if self.verificarDados(self.day_entrada.get()):
				self.dados['day'] = self.day_entrada.get()
				count += 1
			else:
				self.dados['day'] = '0'
				count += 1

			if self.verificarDados(self.month_entrada.get()):
				self.dados['month'] = self.month_entrada.get()
				count += 1
			else:
				self.dados['month'] = '0'
				count += 1

			self.dados['time'] = '0'
			count += 1
		else:
			if self.verificarDados(self.time_entrada.get()):
				self.dados['time'] = self.time_entrada.get()
				count += 1

			self.dados['minute'] = '0'
			count += 1
			self.dados['hour'] = '0'
			count += 1
			self.dados['day'] = '0'
			count += 1
			self.dados['month'] = '0'
			count += 1

		if count == 12:
			db.saveService(self.dados)
			self.destroy()
		else:
			showwarning('Warning!', 'There can be no blank field.')

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

		ClasseBotoes(frame, 'Quit', cmd=self.destroy).pack(side=RIGHT)
		ClasseBotoes(frame, 'Save', cmd=self.salvarDados).pack(side=RIGHT)

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
		

class ClasseFrame(Frame):
	def __init__(self, parent=None, acao='update'):
		super(ClasseFrame, self).__init__(parent)
		self.parent = parent
		self.config(bg="#cccccc", padx=2, pady=2)
		self.pack(fill=BOTH, expand=YES)
		self.lista()

		self.acao = acao

	def lista(self):
		db = Database()
		dados = db.getDataServiceAll()

		scrollbar = Scrollbar(self)
		lista_service = Listbox(self, relief=SUNKEN, font=FONTE_PADRAO_CONTEUDO, bg="#cccccc", fg="black")
		scrollbar.config(command=lista_service.yview)
		lista_service.config(yscrollcommand=scrollbar.set)
		scrollbar.pack(side=RIGHT, fill=Y)
		lista_service.pack(side=LEFT, expand=YES, fill=BOTH)

		opcoes = [ service['name'] for service in dados ]

		for pos, label in enumerate(sorted(opcoes)):
			lista_service.insert(pos, label)

		lista_service.bind('<Double-1>', lambda eventos: self.definirAcao(lista_service.get(lista_service.curselection())))

	def definirAcao(self, service):
		if self.acao == 'update':
			self.updateService(service)
		else:
			self.deleteService(service)

	def updateService(self, service):
		db = Database()
		dados = db.getDataService(service)
		ClasseToplevelPrincipal('Update Service - Schedule Tasks', dados, value=1)
		self.parent.destroy()

	def deleteService(self, service):
		db = Database()
		if askquestion('Warning!', 'Do you want to delete this service?') == 'yes':
			db.deleteService(service)
		self.parent.destroy()


class ClassToplevelList(Toplevel):
	def __init__(self, acao='update', titulo=''):
		super(ClassToplevelList, self).__init__()
		self.title(titulo)

		self.labelTitulo(titulo)
		ClasseFrame(self, acao)
		self.geometry("300x500")

		self.botoes()

		self.resizable(width=False, height=False)
		self.focus_set()
		self.grab_set()
		self.wait_window()
		self.mainloop()

	def labelTitulo(self, titulo):
		Label(self, text=titulo, 
					font=FONTE_PADRAO_LABEL, 
					pady=15).pack(fill=X, expand=YES)

	def botoes(self):
		frame = Frame(self)
		frame.pack()

		ClasseBotoes(self, nome="Quit", cmd=self.destroy).pack(side=RIGHT, fill=X, expand=YES)

class ClasseToplevelView(Toplevel):
	def __init__(self):
		super(ClasseToplevelView, self).__init__()

		self.resizable(width=False, height=False)
		self.conteudo()

		self.focus_set()
		self.grab_set()
		self.wait_window()
		self.mainloop()

	def conteudo(self):
		db = Database()
		frame = Frame(self).grid(row=0, column=0)

		dados = db.getDataServiceAll()
		list_sorted = sorted(dados[i]['name'] for i in range(len(dados)))
		new_list = []
		i = 0
		while i < len(dados):
			if dados[i]['name'] == list_sorted[0]:
				new_list.append(dados[i])
				list_sorted.remove(dados[i]['name'])
				if len(list_sorted) > 0:
					i = -1
				else:
					break
			i += 1

		rotulos = ['name', 'state', 'time', 'count', 'notice', 'mode', 'delete', 'command']
		rotulos_dic = {'name':15, 'state':8, 'time':6, 'count':8, 'notice':10, 'mode':6, 'delete':10, 'command':36}
		i = 1
		cor = FUNDO_PRINCIPAL
		for linha in new_list:
			for c, item in enumerate(rotulos):
				if i % 2 == 0:
					cor = 'black'
				else:
					cor = FUNDO_PRINCIPAL
				if i == 1:
					Label(self, text=item.upper() if item!='count' else 'REPEAT', 
								font=FONTE_PADRAO_LABEL, 
								anchor=W if item=='name' or item=='command' else CENTER,
								width=rotulos_dic[item]).grid(row=i-1, column=c)
				Label(self, text=linha[item],
							anchor=W if item=='name' or item=='command' else CENTER,
							font=FONTE_PADRAO_CONTEUDO, 
							width=rotulos_dic[item], 
							bg=cor).grid(row=i, column=c)
			i += 1

		Button(self, text="Quit", command=self.destroy, 
									font=FONTE_PADRAO_LABEL, 
									cursor='hand2', 
									bd=3,
									relief = GROOVE,
									width=10).grid(row=i+1, column=0, columnspan=10, sticky=E)


class ClasseToplevelSetting(Toplevel):
	def __init__(self, titulo=''):
		super(ClasseToplevelSetting, self).__init__()
		self.title(titulo)
		self.config(padx=15, pady=15)

		db = Database()
		self.dados = db.getDataSetting()

		self.state = self.conteudo()
		self.botoes()

		self.resizable(width=False, height=False)
		self.focus_set()
		self.grab_set()
		self.wait_window()
		self.mainloop()

	def conteudo(self):
		frame = Frame(self, pady=10)
		frame.pack(fill=BOTH, expand=YES)

		ClasseLabel(frame, texto="PID: " + str(self.dados['PID']), w=10, s=TOP)
		ClasseLabel(frame, texto="Time: " + str(self.dados['time']), w=10, s=TOP)
		ClasseLabel(frame, texto="State: ", w=6)

		var_setting = StringVar()
		ClasseRadiobutton(frame, texto="Running", valor="running", var=var_setting).pack(side=LEFT)
		ClasseRadiobutton(frame, texto="Stop", valor="stop", var=var_setting).pack(side=LEFT)

		if self.dados['state'] == 'running':
			var_setting.set('running')
		else:
			var_setting.set('stop')

		return var_setting

	def botoes(self):
		ClasseBotoes(self, nome="Quit", cmd=self.destroy).pack(side=RIGHT)
		ClasseBotoes(self, nome="Update", cmd=self.updateSetting).pack(side=RIGHT)

	def updateSetting(self):
		db = Database()
		self.dados['state'] = self.state.get()
		if askquestion('Warning!', 'Do you want to stop now?') == 'yes':
			db.updateSetting(self.dados)
		self.destroy()


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
				"setting": self.setting,
				"sair": quit
			}
		self.botoes()

	def botoes(self):
		ClasseBotoes(self, 'New', cmd=self.lista['novo']).pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Update', cmd=self.lista['alterar']).pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Delete', cmd=self.lista['apagar']).pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'List', cmd=self.lista['listar']).pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Setting', cmd=self.lista['setting']).pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Exit', cmd=self.lista['sair']).pack(expand=YES, fill=BOTH)

	def newService(self):
		dados = {"name": "", "notice": "", "command": "", "hour": "", "time": "", "count": "", "month": "0", "day": "0", "minute": "", "state": "", "delete": "", "mode": ""}
		ClasseToplevelPrincipal('Create Service - Schedule Tasks', dados)

	def updateService(self):
		ClassToplevelList(titulo='Update Service')

	def deleteService(self):
		ClassToplevelList(acao='delete', titulo="Delete Service")

	def listService(self):
		ClasseToplevelView()

	def setting(self):
		ClasseToplevelSetting(titulo='Setting - Schedule Tasks')

if __name__ == '__main__':
	janela_principal = Tk()
	janela_principal.title("Schedule Tasks")
	janela_principal.resizable(width=False, height=False)

	ClasseLabelPrincipal(janela_principal)

	janela_principal.geometry("250x350")
	janela_principal.mainloop()


