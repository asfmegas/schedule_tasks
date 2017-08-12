#-*- coding: utf-8 -*-

from tkinter import *
import tkinter

FUNDO_PRINCIPAL = '#201d1d'
FONTE_PADRAO_LABEL = ('arial', 18, 'bold')
FONTE_PADRAO_CONTEUDO = ('arial', 18)

class ClasseBotoes(Button):
	def __init__(self, parent=None, nome='', cmd=None):
		super(ClasseBotoes, self).__init__(parent)
		self.config(text=nome, command=cmd, font=('arial', 20, 'bold'), cursor='hand2')

class ClasseRadiobutton(Radiobutton):
	def __init__(self, parent=None, texto='', valor='', var=''):
		super(ClasseRadiobutton, self).__init__(parent)
		self.config(text=texto, variable=var, value=valor, fg='black', font=FONTE_PADRAO_LABEL)
		self.config(highlightcolor="green", wraplength=0, width=10, highlightbackground="grey", relief=SOLID)
		self.config(cursor='hand2', borderwidth=5, activeforeground="green", activebackground="blue", height=1, selectcolor="grey")
		self.config(padx=2, pady=2, anchor=CENTER)

class ClasseToplevelPrincipal(Toplevel):
	def __init__(self, titulo=''):
		super(ClasseToplevelPrincipal, self).__init__()
		self.title(titulo)
		self.config(padx=10, pady=10)

		self.nome_entrada = self.nome()
		self.notice_entrada = self.notice()
		self.state_entrada = self.state()
		self.mode_entrada = self.mode()
		self.repeat_entrada = self.repeat()

		self.time_entrada = self.time()

		self.minute_entrada = self.minute()
		self.hour_entrada = self.hour()
		self.day_entrada = self.day()
		self.month_entrada = self.month()

		self.delete_entrada = self.deleteService()
		self.comando_entrada = self.comando()
		self.botoes()

		self.geometry("900x600")

		""" modal """
		self.focus_set()
		self.grab_set()
		self.wait_window()

	def nome(self):
		frame = Frame(self)
		frame.pack(side=TOP, expand=YES, fill=X)

		label = Label(frame, text="Nome: ", font=FONTE_PADRAO_LABEL)
		label.pack(side=LEFT)

		entrada = Entry(frame, font=FONTE_PADRAO_CONTEUDO)
		entrada.pack(side=LEFT, expand=YES, fill=X)
		entrada.focus()

		return entrada

	def lista(self):
		frame = Frame(self, bg="blue")
		frame.pack(side=TOP, expand=YES, fill=X)

		label = Label(frame, text="Command: ", font=FONTE_PADRAO)
		label.pack(side=LEFT)

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

		label = Label(frame, text="Comando: ", font=FONTE_PADRAO_LABEL)
		label.pack(side=LEFT)

		frame_text = Frame(frame)
		frame_text.pack(side=RIGHT, expand=YES, fill=X)

		entrada = Text(frame_text, font=FONTE_PADRAO_CONTEUDO, height=2)
		entrada.pack(side=LEFT, expand=YES, fill=X)
		entrada.mark_set(INSERT, '1.0')

		return entrada

	def notice(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text='Notice: ', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		var = StringVar()
		notice_yes = ClasseRadiobutton(frame, texto="Yes", valor="yes", var=var).pack(side=LEFT)
		notice_no = ClasseRadiobutton(frame, texto="No", valor="no", var=var).pack(side=LEFT)

		return var

	def state(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text='State: ', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		var = StringVar()
		state_running = ClasseRadiobutton(frame, texto="Running", valor="running", var=var).pack(side=LEFT)
		state_stop = ClasseRadiobutton(frame, texto="Stop", valor="stop", var=var).pack(side=LEFT)

		return var

	def mode(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text='Mode: ', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		var = StringVar()
		repeat = ClasseRadiobutton(frame, texto="Repeat", valor="repeat", var=var)
		repeat.pack(side=LEFT)
		repeat.bind('<Button-1>', lambda eventos: self.controleRepeat())

		date = ClasseRadiobutton(frame, texto="Date", valor="date", var=var)
		date.pack(side=LEFT)
		date.bind('<Button-1>', lambda eventos: self.controleDate())

		return var

	def repeat(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text='Repeat: ', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		entrada = Entry(frame, font=FONTE_PADRAO_CONTEUDO)
		entrada.pack(side=LEFT)
		entrada.config(width=6, justify=CENTER)

		return entrada

	def time(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text='Time: ', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		entrada = Entry(frame, font=FONTE_PADRAO_CONTEUDO)
		entrada.pack(side=LEFT)
		entrada.config(width=6, justify=CENTER)

		return entrada

	def minute(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text='Minute: ', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		entrada = Entry(frame, font=FONTE_PADRAO_CONTEUDO)
		entrada.pack(side=LEFT)
		entrada.config(width=12, justify=CENTER, state=DISABLED)

		return entrada

	def hour(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text='Hour: ', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		entrada = Entry(frame, font=FONTE_PADRAO_CONTEUDO)
		entrada.pack(side=LEFT)
		entrada.config(width=12, justify=CENTER, state=DISABLED)

		return entrada

	def day(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text="Day: ", font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		var = IntVar()
		scale = Scale(frame, variable=var, from_=0,  
									to=31,  
									showvalue=YES, 
									resolution=1, 
									tickinterval=1, 
									orient=HORIZONTAL)
		scale.pack(side=LEFT, expand=YES, fill=X)

		return var

	def month(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text="Month: ", font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		var = IntVar()
		scale = Scale(frame, variable=var, from_=0, 
									to=12,  
									showvalue=YES, 
									resolution=1, 
									tickinterval=1, 
									orient=HORIZONTAL)
		scale.pack(side=LEFT, expand=YES, fill=X)

		return var

	def deleteService(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text="Delete: ", font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		var = StringVar()
		ClasseRadiobutton(frame, texto="Yes", valor="yes", var=var).pack(side=LEFT)
		ClasseRadiobutton(frame, texto="No", valor="no", var=var).pack(side=LEFT)

		return var

	def dados(self):
		print('Nome:', self.nome_entrada.get())
		print('Comando:', self.comando_entrada.get('1.0', END+'-1c'))
		print('Notice:', self.notice_entrada.get())
		print('State:', self.state_entrada.get())
		print('Mode:', self.mode_entrada.get())
		print('Repeat:', self.repeat_entrada.get())

		if self.mode_entrada.get() == 'date':
			print('Minute:', self.minute_entrada.get())
			print('Hour:', self.hour_entrada.get())
			print('Day:', self.day_entrada.get())
			print('Month:', self.month_entrada.get())
		else:
			print('Time:', self.time_entrada.get())

		print('Delete:', self.delete_entrada.get())

	def controleRepeat(self):
		self.time_entrada.config(state=NORMAL)

		self.minute_entrada.config(state=DISABLED)
		self.hour_entrada.config(state=DISABLED)

	def controleDate(self, *widgets):
		self.time_entrada.config(state=DISABLED)

		self.minute_entrada.config(state=NORMAL)
		self.hour_entrada.config(state=NORMAL)

	def botoes(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)
		ClasseBotoes(frame, 'Fechar', cmd=self.destroy).pack(side=RIGHT)
		ClasseBotoes(frame, 'Exibir', cmd=self.dados).pack(side=RIGHT)
		
class ClassToplevelDelete(Toplevel):
	pass

class ClassToplevelList(Toplevel):
	pass

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
		ClasseBotoes(self, 'Apagar').pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Listar').pack(expand=YES, fill=BOTH)
		ClasseBotoes(self, 'Sair', cmd=self.lista['sair']).pack(expand=YES, fill=BOTH)

		# Não fica ordenado como desejado
		# for item in self.lista:
		# 	ClasseBotoes(self, item.upper(), cmd=self.lista[item]).pack(expand=YES, fill=BOTH)

	def newService(self):
		ClasseToplevelPrincipal('Criar Novo Serviço')

	def updateService(self):
		ClasseToplevelPrincipal('Alterar Serviço')

	def deleteService(self):
		pass

	def listService(self):
		pass



if __name__ == '__main__':

	janela_principal = Tk()
	janela_principal.title("Schedule Tasks")

	frame1 = ClasseLabelPrincipal(janela_principal)

	janela_principal.geometry("250x350")
	janela_principal.mainloop()


