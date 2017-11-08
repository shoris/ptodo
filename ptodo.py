import sys
import os

from peewee import *
from datetime import *
import time
from clint.textui import colored, puts

db = SqliteDatabase('tasks.py')

finish_key = "ctrl+Z" if os.name == 'nt' else "ctrl+D"

class Task(Model):
	"""
	Database class
	holds columns for task content, date task is due, 
	and the task's status (whether done or not done)
	"""
	task_content = TextField()
	date_due = DateField()
	is_done = BooleanField()

	class Meta:
		database = db 


def initialize():
	"""Creates database if not already done"""
	db.connect()
	db.create_tables([Task], safe=True)

def start_menu():
	"""Start menu (loop?) with options.""" 

	print "Welcome to ptodo, a very smol todo list app."
	print "Keep track of tasks for work, school, etc.\n\n"
	date = datetime.today().strftime('%Y-%m-%d')
	print "Today is %r\n" % date 
	# print "You have these tasks due >> Show tasks due today
	print "\n"
	print "What would you like to do?\n"
	print "a) Add a task\n"
	print "v) View/Edit/Finish tasks\n"

	while 1:
		answer = raw_input("> ").lower().strip()
		if answer == "a":
			# add new todo to database
			add_task()

		elif answer == "v":
			view_tasks()
		# temporary command so that I can drop and redo table while testing
		elif answer == "d":
			Task.drop_table()

		else:
			print "\nStop entering incorrect characters!"



def view_tasks():
	"""
	User can view tasks.
	"""
	# show tasks in descending chronological order
	shown_tasks = Task.select().order_by(Task.date_due.desc())
	# print shown_tasks

	# makes tasks into list and displays tasks
	index = 0
	size = len(shown_tasks)-1

	while 1:

		task = shown_tasks[index]
		date = task.date_due.strftime("%A %B %d, %Y %I:%M%p ")

		print "\n" 
		print task.task_content, date
		if task.is_done == False:
			print "NOT FINISHED"
		if task.is_done == True:
			print "Finished!"
		print "\n"

		# tell what task this is
		print "\n"
		print "Viewing note " + str(index+1) + " of " + str((size+1))
		print "\n"

		# options
		print "n) next task"
		print "p) previous task"
		print "d) delete task"
		print "f) finish task"
		print "q) to return to the main menu"


		# user input
		next_action = raw_input("Action: [n/p/d/f/q] : ").lower().strip()
		if next_action == 'q':
			start_menu()
		elif next_action == 'd':
			# delete_task
			delete_task(task)
			size -= 1

		elif next_action == 'n':
			if (index + 1) <= size:
				index += 1
			else:
				index = size
		elif next_action == 'p':
			if index >= 1:
				index -= 1
			else:
				index = 0
		elif next_action == 'f':
			finish_task(task)

def add_task():
	""" 
	User names a task with a deadline (date), detail/tontent,
	and is_done boolean is automatically set to False
	"""
	
	todo_string = "Enter in your task (press enter when finished):"
	print todo_string # Will change to colored text with clint later
	todo = raw_input("> ")
	if todo:
		date_string = "When is this task due? (YYYY-mm-dd)"
		print date_string
		# reads data entered from the user
		date = str(raw_input("> "))
		# change date to datetime...thing
		try:
			dt_start = datetime.strptime(date, '%Y-%m-%d')
		except ValueError:
			print "Incorrect format"
		# if something was entered...
		if date:
			Task.create(
				task_content=todo, date_due=date, is_done=False)
			print "Saved successfully!"
			start_menu()
	else:
		print "Nothing entered! Press M to return to main menu."
		choice = raw_input("> ")
		if choice == 'M':
			start_menu()


def finish_task(task):
	"""
	User 'crosses out' a task
	Sets is_done to True
	Called in view_tasks()
	"""
	print "Finish this entry? y/n"
	if raw_input("> ").lower().strip() == 'y':
		task.is_done = True


def delete_task(task):
	"""
	Deletes task from  database.
	"""
	print "Are you sure you want to delete this task? y/n"
	if raw_input("> ").lower().strip() == 'y':
		task.delete_instance()
		print "Deleted!"

if __name__ == "__main__":
	initialize()
	try:
		start_menu()
	except KeyboardInterrupt:
		sys.exit(0)



