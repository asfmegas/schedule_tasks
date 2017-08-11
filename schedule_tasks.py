#-*- coding: utf-8 -*-

__author__ = 'alex.facanha18@gmail.com <asfmegas.github.io>'


from tkinter import *
import tkinter

FUNDO_PRINCIPAL = '#201d1d'
FONTE_PADRAO_LABEL = ('arial', 18, 'bold')
FONTE_PADRAO_CONTEUDO = ('arial', 18)

class ClasseBotoes(Button):
	def __init__(self, parent=None, nome='', cmd=None):
		super(ClasseBotoes, self).__init__(parent)
		self.config(text=nome, command=cmd, font=('arial', 20, 'bold'), cursor='hand2')

class ClasseToplevelPrincipal(Toplevel):
	def __init__(self, titulo=''):
		super(ClasseToplevelPrincipal, self).__init__()
		self.title(titulo)
		self.config(padx=10, pady=10)

		self.nome_entrada = self.nome()
		self.comando_entrada = self.comando()
		self.notice_entrada = self.notice()
		self.state_entrada = self.state()
		self.mode_entrada = self.mode()
		self.botoes()

		self.geometry("900x500")

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
		notice_yes = Radiobutton(frame, text='Yes', variable=var, value='yes', fg='black', font=FONTE_PADRAO_LABEL).pack(side=LEFT)
		notice_no = Radiobutton(frame, text='No', variable=var, value='no', fg='black', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		return var

	def state(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text='State: ', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		var = StringVar()
		state_running = Radiobutton(frame, text='Running', variable=var, value='running', fg='black', font=FONTE_PADRAO_LABEL).pack(side=LEFT)
		state_stop = Radiobutton(frame, text='Stop', variable=var, value='stop', fg='black', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		return var

	def mode(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)

		label = Label(frame, text='Mode: ', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		var = StringVar()
		mode_repeat = Radiobutton(frame, text='Repeat', variable=var, value='repeat', fg='black', font=FONTE_PADRAO_LABEL).pack(side=LEFT)
		mode_date = Radiobutton(frame, text='Date', variable=var, value='date', fg='black', font=FONTE_PADRAO_LABEL).pack(side=LEFT)

		# if var.get() == 'date':
		# 	self.desabilitar([self.])

		return var

	def dados(self):
		print(self.nome_entrada.get())
		print(self.comando_entrada.get('1.0', END+'-1c'))
		print(self.notice_entrada.get())
		print(self.state_entrada.get())
		print(self.mode_entrada.get())

	def desabilitar(self, *lista):
		for item in lista:
			item.config(state=DISABLED)

	def habilitar(self):
		self.nome_entrada.config(state=NORMAL)


	def botoes(self):
		frame = Frame(self)
		frame.pack(expand=YES, fill=X)
		ClasseBotoes(frame, 'Fechar', cmd=self.destroy).pack(side=RIGHT)
		ClasseBotoes(frame, 'Exibir', cmd=self.dados).pack(side=RIGHT)
		# ClasseBotoes(frame, 'Desabilitar', cmd=lambda: self.desabilitar(self.notice_entrada)).pack(side=RIGHT)
		# ClasseBotoes(frame, 'Hbilitar', cmd=self.habilitar).pack(side=RIGHT)


		
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
		ClasseToplevelPrincipal('Novo Serviço')

	def updateService(self):
		ClasseToplevelPrincipal('Alterar Serciço')

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




