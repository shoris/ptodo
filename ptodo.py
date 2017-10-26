import sys
import os

from peewee import *
from datetime import *
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
	# task_category = CharField()

	class Meta:
		database = db 


def initialize():
	"""Creates database if not already done"""
	db.connect()
	db.create_tables([Task], safe=True)

def start_menu():
	"""Start menu (loop?) with options.""" 
	while 1: 
		print "Welcome to ptodo, a very smol todo list app."
		print "Keep track of tasks for work, school, etc.\n\n"
		date = datetime.today().strftime('%Y-%m-%d')
		print "Today is %r\n" % date 
		print "You have these tasks due:" 
		# Show tasks due today
		print "\n"
		print "What would you like to do?\n"
		print "A > Add a task\n"
		print "V > View/Edit/Finish tasks\n"

		answer = raw_input("> ")
		if answer == "A":
			# add new todo to database
			add_task()

		elif answer == "V":
			view_tasks()
		elif answer == "D":
			Task.drop_table()
		else:
			print "\nStop entering incorrect characters!"



def view_tasks():
	"""
	User can view tasks.
	"""
	# Displays tasks for today/or unfinished tasks
	for task in Task.select():
		print "\n\n"
		print task.task_content, task.date_due, task.is_done
		print "\n\n"

	# List of options:
	# Finish a task 
	# Add a task
	# Delete a task
	# (More options?)
	# View all tasks
	# View unfinished tasks
	# View finished tasks
	# View tasks for today
	# Enter in a date
	pass 

def add_task():
	""" 
	User names a task with a deadline (date), detail/tontent,
	and is_done boolean is automatically set to False
	"""
	# get info from user
	# print "What do you need to get done? (Y-m-d)"
	# task_title = raw_input("> ")
	# print "On what date is it due?"
	# date_task = raw_input("> ")
	# print "Category?"
	# new_category = raw_input("> ")

	# task1 = Task.create(task_content=task_title, date_due=date_task, task_category=new_category, is_done=False)
	# task1.save()

	
	todo_string = "Enter in your task (press enter when finished):"
	print todo_string # Will change to colored text with clint later
	todo = raw_input("> ")
	if todo:
		date_string = "When is this task due?"
		print date_string
		# reads data entered from the user
		date = raw_input("> ")
		# if something was entered...
		if date:
			Task.create(
				task_content=todo, date_due=date, is_done=False)
			print "Saved successfully!"
	else:
		print "Nothing entered! Press M to return to main menu."
		choice = raw_input("> ")
		if choice == 'M':
			start_menu()


def finish_task():
	"""
	User 'crosses out' a task
	Sets is_done to True
	"""
	pass

def delete_task():
	"""
	Deletes task from  database.
	"""
	pass 



if __name__ == "__main__":
	initialize()
	try:
		start_menu()
	except KeyboardInterrupt:
		sys.exit(0)



