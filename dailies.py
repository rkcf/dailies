# Dailies
# A simple command line utility for keeping track of daily tasks.
# Copyright (C) 2016 Andrew Steinke

import sys
import os
import csv
import datetime

data_path = os.environ['HOME'] + '/.dailies'

def load_data():
    """Loads csv task data into dicts, and places them in the master list."""
    if os.path.isfile(data_path):
        task_list = []
        with open(data_path, 'r') as f:
            parser = csv.DictReader(f)
            for row in parser:
                row['total'] = int(row['total'])
                row['streak'] = int(row['streak'])
                row['max_streak'] = int(row['max_streak'])
                row['date_completed'] = int(row['date_completed'])
                task_list.append(row)
        return(task_list)
    else:
        print('Datafile not found, creating one at $HOME/.dailies')
        save_data([])
        return([])

def clean_streaks(list):
    """Checks whether any streaks are stale, and resets counter to 0 if so."""
    today_ord = datetime.date.today().toordinal()
    for d in list:
        if today_ord - d['date_completed'] > 1:
            d['streak'] = 0

def parse_args(list):
    """Parses arguments from command line and invokes proper function."""
    arg_cnt = len(sys.argv) - 1
    if arg_cnt < 1 or arg_cnt > 2: 
        print('ERROR: Incorrect number of arguments!')
        print_help()
    elif sys.argv[1] == 'add': 
        if arg_cnt == 2:
            add_task(sys.argv[2], list)
        else:
            print('ERROR: add requires an argument!')
    elif sys.argv[1] == 'complete': 
        if arg_cnt == 2:
            complete_task(sys.argv[2], list)
        else:
            print('ERROR: complete requires an argument!')
    elif sys.argv[1] == 'rm':
        if arg_cnt == 2:
            remove_task(sys.argv[2], list)
        else:
            print('ERROR: rm requires an argument!')
    elif sys.argv[1] == 'list': 
        list_all(list)
    elif sys.argv[1] == 'help': 
        print_help()
    else:
        print('ERROR: Invalid command!')
        print_help()

def list_all(list):
    """Prints a table with tasks and stats."""
    print ('{0:10} | {1:5} | {2:6} | {3:5}'.format('Task', 'Total', 'Streak', 'Max Streak'))
    for d in list:
        print ('{0:10} | {1:5} | {2:6} | {3:5}'.format(d['name'], d['total'], d['streak'], d['max_streak']))


def add_task(name, list):
    """Adds new task to list."""
    task = {'name': name,
            'total': 0,
            'streak': 0,
            'max_streak': 0,
            'date_completed': 0
           }
    if dict_in_list(name, list):
        print('ERROR: Task is already in list!')
    else:
        list.append(task)

def remove_task(name, list):
    """Removes task from list."""
    if dict_in_list(name, list):
        while True:
            confirm = input('Are you sure you want to permenantly delete this task [y/n]?')
            if confirm == 'y':
                for d in list:
                    if d['name'] == name:
                        list.remove(d)
                break
            elif confirm == 'n':
                break
            else:
                confirm = input('[y/n]?')
    else:
        print('ERROR: Task not found!')

def complete_task(name, list):
    """Adds one to the task's total, checks if a streak is occuring."""
    for d in list:
        if d['name'] == name:
            d['total'] += 1
            today_ord = datetime.date.today().toordinal()
            if d['date_completed'] != today_ord:
                d['streak'] +=1
            if d['streak'] > d['max_streak']:
                d['max_streak'] = d['streak']
            d['date_completed'] = today_ord

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
        fieldnames = ['name', 'total', 'streak', 'max_streak', 'date_completed']       
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for d in list:
            writer.writerow(d) 

def dict_in_list(name, list):
    """Check if the dict is in the list."""
    for d in list:
        if d['name'] == name:
            return True
    return False

def main():
    task_list = load_data()
    clean_streaks(task_list)
    parse_args(task_list)
    save_data(task_list)

main()
