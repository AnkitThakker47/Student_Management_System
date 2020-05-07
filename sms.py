from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
import matplotlib.pyplot as plt
import socket
import requests
from sqlite3 import *
import bs4
import lxml



def alter(msg):
	if msg.find(',') != -1 or msg.find(';') != -1:
		motd = msg.replace(',' , '\n')
		motd = msg.replace(';' , '\n')
	else:
		motd, i, j = '', 0, 0
		mesappend = ''
		val = msg.rfind('-')
		partone = msg[0:val]
		parttwo = msg[val:]
		#print(partone,'\n',parttwo)
		for k in partone:
			#print(k)
			if k  == ' ' and j % 6 == 0:
				mesappend = mesappend + k + '\n'
				j += 1
			elif k == ' ':
				mesappend = mesappend + k
				j += 1
			else:
				mesappend = mesappend + k
		motd = mesappend + '\n' + parttwo
	#print(motd)
	return motd
def f1():
	root.withdraw()
	adst.deiconify()

def f2():
	vistData.delete(1.0, END)
	root.withdraw()
	vist.deiconify()
	con = None
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		sql = "select * from student"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "rno: " + str(d[0]) + "   name: "+str(d[1]) + "     marks: "+ str(d[2]) +"\n"
		vistData.insert(INSERT, info)
	except Exception as e:
		print("Issue ",e)
	finally:
		if con is not None:
			con.close()	
def f3():
	adst.withdraw()
	root.deiconify()
	
def f4():
	vist.withdraw()
	root.deiconify()

def f5():
	root.withdraw()
	upst.deiconify()


def f6():
	upst.withdraw()
	root.deiconify()

def f7():
	root.withdraw()
	dest.deiconify()

def f8():
	dest.withdraw()
	root.deiconify()

def f9():
	con = None
	student, marks = [],[]
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		sql = "SELECT * FROM student ORDER BY marks LIMIT 5"
		data = cursor.execute(sql)
		for d in data:
			student.append(d[1])
			marks.append(int(d[2]))
		plt.bar(student, marks)
		plt.ylabel('Marks')
		plt.title("Batch Information")
		plt.grid()
		plt.show()
	except Exception as e:
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()



def f10():
	con = None
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		if rnoEnter.get() == '':
			raise Exception("Roll number cannot be empty")
		if not rnoEnter.get().isdigit():
			rnoEnter.delete(0, END)
			raise Exception("Roll number should only contains digit")
		rno, name= int(rnoEnter.get()), nameEnter.get()
		if rno < 1:
			rnoEnter.delete(0, END)
			raise Exception("Roll number cannot be 0 or negative")
		if len(name) < 2:
			nameEnter.delete(0, END)
			raise Exception("Length of name should not be less than 2")
		if marksEnter.get() == '':
			raise Exception("Marks cannot be empty")
		if not marksEnter.get().isdigit():
			marksEnter.delete(0, END)
			raise Exception("Marks should contains only digit")
		marks = int(marksEnter.get())
		if marks < 0 or marks > 100:
			marksEnter.delete(0, END)
			raise Exception("Marks out of range")
		args = (rno, name, marks)
		sql = "insert into student values ('%d', '%s', '%d')"
		cursor.execute(sql % args)
		con.commit()
		showinfo("Success",str(rno) + " Record added")
		rnoEnter.delete(0, END)
		marksEnter.delete(0, END)
		nameEnter.delete(0, END)
	except Exception as e:
		con.rollback()
		showerror("Issue",e)
	finally:
		if con is not None:
			con.close()

def f11():
	con = None
	args = ()
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		sql, args  = '', ()
		if urnoEnter.get() == '':
			raise Exception("Roll number cannot be empty")
		if not urnoEnter.get().isdigit():
			urnoEnter.delete(0, END)
			raise Exception("Roll number should contain only digits")
		rno = int(urnoEnter.get())
		if rno < 1:
			urnoEnter.delete(0, END)
			raise Exception("Roll number cannot be 0 or negative")
		if unameEnter.get() != '' and umarksEnter.get() != '':
			if len(unameEnter.get()) < 2:
				unameEnter.delete(0, END)
				raise Exception("Length of the name cannot be less than 2")
			if not umarksEnter.get().isdigit():
				umarksEnter.delete(0, END)
				raise Exception("Roll number should contain digits only")
			marks = int(umarksEnter.get())
			if marks < 0 or marks > 100:
				umarksEnter.delete(0, END)
				raise Exception("Marks out of Range")
			name = unameEnter.get()
			args = (name, marks, rno)
			sql = "UPDATE student SET name = '%s', marks = '%d' WHERE rno = '%d'"
		elif unameEnter.get() != '' and umarksEnter.get() == '':
			if len(unameEnter.get()) < 2:
				unameEnter.delete(0, END)
				raise Exception("Length of name should not be less than 2")
			name = unameEnter.get()
			args =  (name, rno)
			sql = "UPDATE student SET name = '%s' WHERE rno = '%d'"
		elif unameEnter.get() == '' and umarksEnter.get() != '':
			if not umarksEnter.get().isdigit():
				umarksEnter.delete(0, END)
				raise Exception("Marks should be digits only")
			marks = int(umarksEnter.get())
			if marks < 0 or marks > 100:
				umarksEnter.delete(0, END)
				raise Exception("Marks out of range")
			args = (marks, rno)
			sql = "UPDATE student SET marks = '%d' WHERE rno = '%d'"
		else:
			raise Exception("Enter the values to be updated")
		cursor.execute(sql % args)
		if cursor.rowcount == 0:
			raise Exception(str(rno) + " not found")
		con.commit()
		showinfo("Success",str(rno) + " Record updated")
		urnoEnter.delete(0, END)
		umarksEnter.delete(0, END)
		unameEnter.delete(0, END)
	except Exception as e:
		con.rollback()
		showerror("Issue",e)
	finally:
		if con is not None:
			con.close()
	
def f12():
	con = None
	try:
		con = connect("stu_test.db")
		cursor = con.cursor()
		if drnoEnter.get() == '':
			raise Exception('Roll number cannot be empty')
		if not drnoEnter.get().isdigit():
			raise Exception("Roll number should be digits only")
		rno = int(drnoEnter.get())
		if rno < 1:
			raise Exception('Roll number cannot be 0 or negative')
		args = (rno)
		sql = "delete from student where rno = '%d'"
		cursor.execute(sql % args)
		if cursor.rowcount == 0:
			raise Exception(str(rno) + " not found")
		con.commit()
		showinfo("Success",str(rno) + " deleted successfully")
	except Exception as e:
		con.rollback()
		showerror("Issue", e)
	finally:
		if con is not None:
			con.close()
		drnoEnter.delete(0, END)


info, qotd = '',''
try:
	socket.create_connection(("www.google.com", 80))
	res = requests.get("https://ipinfo.io")
	data = res.json()
	city_name = data['city']
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city_name 
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	res = requests.get(a1 + a2 + a3)
	data = res.json()
	temp = data['main']['temp']
	info = "Location: " + str(city_name) + "\tTemprature: " + str(temp)
	res = requests.get("https://www.brainyquote.com/quote_of_the_day")
	soup = bs4.BeautifulSoup(res.text,'lxml')
	data = soup.find("img", {"class": "p-qotd"})
	msg = data['alt']
	msg = alter(msg)
	qotd = "QOTD: " + str(msg)
except Exception as e:
	showerror("Connection issue",e)
	print(e)

root = Tk()
root.title("Student Management System")
root.geometry("508x550+400+25")
root.configure(background = "#B8CDCD")


btnAdd = Button(root, text="Add", font = ("Arial", 18, "bold"), width = 10,command = f1)
btnView = Button(root, text="View", font = ("Arial", 18, "bold"), width = 10,command = f2)
btnUpdate = Button(root, text="Update", font = ("Arial", 18, "bold"), width = 10, command = f5)
btnDelete = Button(root, text="Delete", font = ("Arial", 18, "bold"), width = 10, command = f7)
btnCharts = Button(root, text="Charts", font = ("Arial", 18, "bold"), width = 10, command = f9)
lblInfo = Label(root, text = info, font = ('Arial', 18, 'bold'), borderwidth = 1, bg = "#B8CDCD", relief = "solid")
lblQotd = Label(root, text = qotd, font = ('Arial', 18, 'bold'), borderwidth = 1, bg = "#B8CDCD", relief = "solid")
btnAdd.pack(pady = 10)
btnView.pack(pady = 10)
btnUpdate.pack(pady = 10)
btnDelete.pack(pady = 10)
btnCharts.pack(pady = 10)
lblInfo.pack(pady = 10)
lblQotd.pack(pady = 10)


adst = Toplevel(root)
adst.title("Add student")
adst.geometry("500x500+400+100")
adst.configure(background="#ADCCDE")
adst.withdraw()

lblrno = Label(adst, text = "enter rno:", font = ('Arial', 18, 'bold'), bg = "#ADCCDE")
rnoEnter = Entry(adst, bd = 5 ,font = ('Arial', 18, 'bold'))
lblname = Label(adst, text = "enter name:", font = ('Arial', 18, 'bold'), bg = "#ADCCDE")
nameEnter = Entry(adst, bd = 5 ,font = ('Arial', 18, 'bold'))
lblmarks = Label(adst, text = "enter marks:", font = ('Arial', 18, 'bold'), bg = "#ADCCDE")
marksEnter = Entry(adst, bd = 5 ,font = ('Arial', 18, 'bold'))
adstSave = Button(adst, text="Save", font = ("arial", 18, "bold"), command = f10)
adstBack = Button(adst, text="Back", font = ("arial", 18, "bold"), command = f3)
lblrno.pack(pady = 10)
rnoEnter.pack(pady = 10)
lblname.pack(pady = 10)
nameEnter.pack(pady = 10)
lblmarks.pack(pady = 10)
marksEnter.pack(pady = 10)
adstSave.pack(pady = 10)
adstBack.pack(pady = 10)
rnoEnter.focus()

vist = Toplevel(root)
vist.title("View student")
vist.geometry("500x500+400+100")
vist.withdraw()
vist.configure(background = "#D2D0C3")

vistData = ScrolledText(vist, width = 40, height = 20)
vistBack = Button(vist, text = "Back", font= ("arial", 18, "bold"), command = f4)

vistData.pack(pady = 10)
vistBack.pack(pady = 10)


upst = Toplevel(root)
upst.title("Update Student")
upst.geometry("500x500+400+100")
upst.withdraw()
upst.configure(background="#CDC8CA")
upst.withdraw()

ulblrno = Label(upst, text = "enter rno:", font = ('Arial', 18, 'bold'), bg = "#CDC8CA")
urnoEnter = Entry(upst, bd = 5 ,font = ('Arial', 18, 'bold'))
ulblname = Label(upst, text = "enter name:", font = ('Arial', 18, 'bold'), bg = "#CDC8CA")
unameEnter = Entry(upst, bd = 5 ,font = ('Arial', 18, 'bold'))
ulblmarks = Label(upst, text = "enter marks:", font = ('Arial', 18, 'bold'), bg = "#CDC8CA")
umarksEnter = Entry(upst, bd = 5 ,font = ('Arial', 18, 'bold'))
uadstSave = Button(upst, text="Save", font = ("arial", 18, "bold"), command = f11)
uadstBack = Button(upst, text="Back", font = ("arial", 18, "bold"), command = f6)
ulblrno.pack(pady = 10)
urnoEnter.pack(pady = 10)
ulblname.pack(pady = 10)
unameEnter.pack(pady = 10)
ulblmarks.pack(pady = 10)
umarksEnter.pack(pady = 10)
uadstSave.pack(pady = 10)
uadstBack.pack(pady = 10)
urnoEnter.focus()

dest = Toplevel(root)
dest.title("Delete Student")
dest.geometry("500x500+400+100")
dest.withdraw()
dest.configure(background = "#ADCCDE")

dlblrno = Label(dest, text="enter rno:", font = ('Arial', 18, 'bold'), bg="#ADCCDE")
drnoEnter = Entry(dest, font = ('Arial', 18, 'bold'), bd = 5)
destSave = Button(dest, text = "Save" ,font = ('Arial', 18, 'bold'), command = f12)
destBack = Button(dest, text = "Back", font = ('Arial', 18, 'bold'), command = f8)
dlblrno.pack(pady = 10)
drnoEnter.pack(pady = 10)
destSave.pack(pady = 10)
destBack.pack(pady = 10)
drnoEnter.focus()

root.mainloop()