# Dailies
# A simple command line utility for keeping track of daily tasks.

import sys
import os
import csv

task_list = []
data_path = os.environ['HOME'] + '/.dailies'
# name, total, current_streak, max_streak, date_last_completed

def load_data():
    """Loads csv task data into dicts, and places them in the master list"""
    if os.path.isfile(data_path):
        with open(data_path, 'r') as f:
            parser = csv.DictReader(f)
            for row in parser:
                task_list.append(row)
    else:
        print('Datafile not found, creating one at $HOME/.dailies')
        #TODO create base datafile

# TODO Cleanup Streaks
# Checks each tasks date_last_complete against current date, if it is two
# days previous, the current_streak is reset to 0.

def parse_args():
    """Parses arguments from command line and invokes proper function"""
    arg_cnt = len(sys.argv) - 1
    if arg_cnt < 1 and arg_cnt > 2: 
        print(arg_cnt)
        print('ERROR: Incorrect number of arguments!')
        print_help()
    elif sys.argv[1] == 'add': 
        if arg_cnt == 2:
            add_task(sys.argv[2])
        else:
            print('ERROR: add requires an argument!')
    elif sys.argv[1] == 'rm':
        if arg_cnt == 2:
            remove_task(sys.argv[2])
        else:
            print('ERROR: rm requires an argument!')
    elif sys.argv[1] == 'list': 
        list_all()
    elif sys.argv[1] == 'help': 
        print_help()
    else:
        print('ERROR: Invalid command!')
        print_help()

def list_all():
    """Prints a table with tasks and stats."""
    print ('{0:5} | {1:5}'.format('Task', 'Total'))
    for task in task_list:
        print ('{0:5} | {1:5}'.format(task['name'], task['total']))

#TODO Today Command: Print each task that needs to be done yet today.

def add_task(name):
    """Adds new task to list."""
    task = {'name': name,
            'total': 0,
           }
    task_list.append(task)

def remove_task(task):
    """Removes task from list."""
    if task_list.count(task) == 1:
        while True:
            confirm = input('Are you sure you want to permenantly delete this task [y/n]?')
            if confirm == 'y':
                task_list.remove(task)
                break
            elif confirm == 'n':
                break
            else:
                confirm = input('[y/n]?')
    else:
        print('ERROR: Task not found!')


#TODO Complete Command: Updates date_last_completed value of task to todays
# date.  Increments total.  Adds one to current_streak, and updates
# max_streak as needed.

def print_help():
    """Prints list of commands with descriptions."""
    print('help')

def save_data():
    """Writes task data to file"""
    with open(data_path, 'w') as f:
        # name, total, current_streak, max_streak, date_last_completed
        fieldnames = ['name', 'total']       
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for dict in task_list:
            writer.writerow(dict) 

def main():
    load_data()
    parse_args()
    save_data()

main()
