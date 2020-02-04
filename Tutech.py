from tkinter import *
from tkinter import ttk
import shelve
tutors=shelve.open('tutors')
if(list(tutors.keys())!=['tutors']):
	tutors['tutors']=[]
class Base(Tk):
	def __init__(self):
		Tk.__init__(self)
		Tk.wm_title(self,'TuTech')
		container = Frame(self)
		container.pack(side='top',fill='both',expand=True)
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)
		self.frames = {}
		for F in (StartPage,PageOne,LoginPage,AdminPage,AddTutor,ShowTutor,RemoveTutor,StudentPage):
			frame = F(container,self)
			self.frames[F]=frame
			frame.grid(row=0,column=0,sticky='nsew')
		self.show_frame(StartPage)
	def show_frame(self,cont):
		frame = self.frames[cont]
		frame.tkraise()
		try:
			frame.display()
		except:
			pass
class StartPage(Frame):
	def __init__(self, parent, controller):
		Frame.__init__(self,parent)
		label = Label(self,text="Welcome to TuTech")
		label.pack()
		ttk.Button(self, text='Get Started',command=lambda:controller.show_frame(PageOne)).pack()
class PageOne(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		Label(self,text='Select User').grid(row=0,column=0)
		ttk.Button(self,text='Administrator',command=lambda:controller.show_frame(LoginPage)).grid(row=1,column=0)
		ttk.Button(self,text='Student',command=lambda:controller.show_frame(StudentPage)).grid(row=2,column=0)
class LoginPage(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.controller=controller
		Label(self,text='Username').grid(row=0,column=0,sticky='E',pady=5)
		Label(self,text='Password').grid(row=1,column=0,sticky='E',pady=5)
		self.user=''
		self.passw=''
		self.userfield = ttk.Entry(self,textvariable=self.user,width=25)
		self.userfield.grid(row=0,column=1,pady=5)
		self.userfield.focus()
		self.passfield = ttk.Entry(self,textvariable=self.passw,width=25,show='\u2022')
		self.passfield.grid(row=1,column=1,pady=5)
		ttk.Button(self,text='Login',command=lambda:self.check_creds()).grid(row=2,column=0,columnspan=2,pady=5)
		self.message = Label(self,text='Incorrect Username or Password')
		ttk.Button(self,text='Back',command=lambda:controller.show_frame(PageOne)).grid(row=4,column=0,columnspan=2,pady=5)
	def display(self):
		self.userfield.delete(0,END)
		self.passfield.delete(0,END)
		self.message.grid_forget()
		self.userfield.focus()
	def check_creds(self):
		if(self.userfield.get()=='admin' and self.passfield.get()=='123'):
			self.userfield.delete(0,END)
			self.passfield.delete(0,END)
			self.message.grid_forget()
			self.controller.show_frame(AdminPage)
		else:
			self.message.grid(row=3,column=0,columnspan=2)
class AdminPage(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		ttk.Button(self,text='Add Tutor',command=lambda:controller.show_frame(AddTutor)).pack()
		ttk.Button(self,text='Show Tutors',command=lambda:controller.show_frame(ShowTutor)).pack()
		ttk.Button(self,text='Remove Tutor',command=lambda:controller.show_frame(RemoveTutor)).pack()
		ttk.Button(self,text='Logout',command=lambda:controller.show_frame(LoginPage)).pack()
class AddTutor(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.controller=controller
		Label(self,text='Name').grid(row=0,column=0,sticky='E')
		self.namefield = ttk.Entry(self,width=25)
		self.namefield.grid(row=0,column=1)
		Label(self,text='Area').grid(row=1,column=0,sticky='E')
		self.subjects=['Choose subject','Maths','English','Computer','Physics','Chemistry','Biology','History','Geography']
		self.sub=StringVar()
		self.sub.set(self.subjects[0])
		self.list=ttk.OptionMenu(self,self.sub,*self.subjects)
		self.list.grid(row=3,column=1)
		Label(self,text='Fees Rs.').grid(row=2,column=0,sticky='E')
		self.areafield = ttk.Entry(self,width=25)
		self.areafield.grid(row=1,column=1)
		Label(self,text='Subject').grid(row=3,column=0,sticky='E')
		self.feefield = ttk.Entry(self,width=25)
		self.feefield.grid(row=2,column=1)
		ttk.Button(self,text='Add',command=lambda:self.add()).grid(row=4,column=0,columnspan=2)
		ttk.Button(self,text='Back',command=lambda:controller.show_frame(AdminPage)).grid(row=5,column=0,columnspan=2)
	def add(self):
		if(self.sub.get()!=self.subjects[0]):
			s=self.namefield.get()+','+str(self.sub.get())+','+self.areafield.get()+','+self.feefield.get()
			lst=tutors['tutors']
			lst.append(s)
			tutors['tutors']=lst
			self.controller.show_frame(AdminPage)
	def display(self):
		self.namefield.delete(0,END)
		self.sub.set(self.subjects[0])
		self.areafield.delete(0,END)
		self.feefield.delete(0,END)
class ShowTutor(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		Label(self,text='Name').grid(row=0,column=0)
		Label(self,text='Subject').grid(row=0,column=1)
		Label(self,text='Area').grid(row=0,column=2)
		Label(self,text='Fees').grid(row=0,column=3)
		self.labels=[]
		self.back=ttk.Button(self,text='Back',command=lambda:controller.show_frame(AdminPage)).grid(row=1000,column=0,columnspan=2)
	def display(self):
		i=1
		for lb in self.labels:
			lb.grid_forget()
		self.labels.clear()
		for T in tutors['tutors']:
			if len(T)>1:
				name,subj,area,fee=T.split(',')
				subj=subj.replace('\n','')
				lb=ttk.Label(self,text=name)
				lb.grid(row=i,column=0)
				lb2=ttk.Label(self,text=subj)
				lb2.grid(row=i,column=1)
				lb3=ttk.Label(self,text=area)
				lb3.grid(row=i,column=2)
				lb4=ttk.Label(self,text=fee)
				lb4.grid(row=i,column=3)
				self.labels.extend([lb,lb2,lb3,lb4])
				i=i+1
		self.back.grid(row=i,column=0,columnspan=2)
class RemoveTutor(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.controller=controller
		self.sub=StringVar()
		self.sub.set('Choose Tutor')
		self.list=ttk.OptionMenu(self,self.sub,[])
		self.list.grid(row=0,column=0)
		ttk.Button(self,text='Remove',command=lambda:self.removetut()).grid(row=1,column=0)
		ttk.Button(self,text='Back',command=lambda:controller.show_frame(AdminPage)).grid(row=2,column=0)
	def display(self):
		f=tutors['tutors']
		f.insert(0,'Choose Tutor')
		self.list=ttk.OptionMenu(self,self.sub,*f)
		self.list.grid(row=0,column=0)
	def removetut(self):
		lst=tutors['tutors']
		lst.remove(self.sub.get())
		tutors['tutors']=lst
		self.controller.show_frame(AdminPage)
class StudentPage(Frame):
	def __init__(self,parent,controller):
		Frame.__init__(self,parent)
		self.controller=controller
		Label(self,text='Subject').grid(row=0,column=0,sticky='E')
		self.labels=[]
		self.subjects=['Choose subjects','Maths','English','Computer','Physics','Chemistry','Biology','History','Geography']
		self.sub=StringVar()
		self.sub.set(self.subjects[0])
		self.list=ttk.OptionMenu(self,self.sub,*self.subjects)
		self.list.grid(row=0,column=1)
		ttk.Button(self,text='Show',command=lambda:self.show()).grid(row=1,column=0,columnspan=2)
		self.back=ttk.Button(self,text='Back',command=lambda:controller.show_frame(PageOne))
		self.notutors=ttk.Label(self,text='No Tutors Available')
		self.notutors.grid_forget()
		self.back.grid(row=1000,column=0,columnspan=2)
	def show(self):
		if(self.sub.get()!=self.subjects[0]):
			i=2
			for l in self.labels:
				l.grid_forget()
			self.labels.clear()
			for T in tutors['tutors']:
				if len(T)>1:
					name,subj,area,fee=T.split(',')
					if(subj==self.sub.get()):
						lb=ttk.Label(self,text=name)
						lb.grid(row=i,column=0)
						lb2=ttk.Label(self,text=area)
						lb2.grid(row=i,column=1)
						lb3=ttk.Label(self,text=fee)
						lb3.grid(row=i,column=2)
						self.labels.extend([lb,lb2,lb3])
						i=i+1
			if(i==2):
				self.notutors.grid(row=i,column=0,columnspan=2)
				self.back.grid(row=i+1,column=0,columnspan=2)
			else:
				self.notutors.grid_forget()
				self.back.grid(row=i,column=0,columnspan=2)
	def display(self):
		self.sub.set(self.subjects[0])
		for l in self.labels:
			l.grid_forget()
		self.labels.clear()
		self.notutors.grid_forget()
def close_file():
	tutors.close()
	app.destroy()
app=Base()
app.protocol("WM_DELETE_WINDOW",close_file)
app.mainloop()