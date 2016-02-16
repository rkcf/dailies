# Dailies
# A simple command line utility for keeping track of daily tasks.
# Copyright (C) 2016 Andrew Steinke

import sys
import os
import csv

task_list = []
data_path = os.environ['HOME'] + '/.dailies'

def load_data():
    """Loads csv task data into dicts, and places them in the master list"""
    if os.path.isfile(data_path):
        with open(data_path, 'r') as f:
            parser = csv.DictReader(f)
            for row in parser:
                row['total'] = int(row['total'])
                task_list.append(row)
    else:
        print('Datafile not found, creating one at $HOME/.dailies')
        save_data([])

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
    elif sys.argv[1] == 'complete': 
        if arg_cnt == 2:
            complete_task(sys.argv[2])
        else:
            print('ERROR: complete requires an argument!')
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
    print ('{0:10} | {1:10}'.format('Task', 'Total'))
    for task in task_list:
        print ('{0:10} | {1:5}'.format(task['name'], task['total']))

def add_task(name):
    """Adds new task to list."""
    task = {'name': name,
            'total': 0,
           }
    if is_task(name):
        print('ERROR: Task is already in list!')
    else:
        task_list.append(task)

def remove_task(task):
    """Removes task from list."""
    if is_task:
        while True:
            confirm = input('Are you sure you want to permenantly delete this task [y/n]?')
            if confirm == 'y':
                for d in task_list:
                    if d['name'] == task:
                        task_list.remove(d)
                break
            elif confirm == 'n':
                break
            else:
                confirm = input('[y/n]?')
    else:
        print('ERROR: Task not found!')

def complete_task(name):
    """Adds one to the task's total"""
    for d in task_list:
        if d['name'] == name:
            d['total'] += 1

def print_help():
    """Prints list of commands with descriptions."""

    help_text = """Dailies
A simple command line utility for keeping track of daily tasks.

Commands:
    help    Print this text.
    add     Add a new daily.  Takes a task name argument.
    rm      Permenantly remove a daily.  Takes a task name argument.
    complete Mark a task complete.  Takes a task name argument.
    list    Display all dailies and their stats""" 

    print(help_text)

def save_data(list):
    """Writes list of dicts to file."""
    with open(data_path, 'w') as f:
        # name, total, current_streak, max_streak, date_last_completed
        fieldnames = ['name', 'total']       
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for dict in list:
            writer.writerow(dict) 

def is_task(name):
    """Given a task name check if the task dict is in the list."""
    for d in task_list:
        if d['name'] == name:
            return True
    return False

def main():
    load_data()
    parse_args()
    save_data(task_list)

main()
