# Dailies
# A simple command line utility for keeping track of daily tasks.
# Copyright (C) 2016 Andrew Steinke

import sys
import os
import csv
import datetime

DATA_PATH = os.environ['HOME'] + '/.dailies'
TODAY_ORD = datetime.date.today().toordinal()

def load_data():
    """Loads csv task data into dicts, and places them in a list."""
    if os.path.isfile(DATA_PATH):
        task_list = []
        with open(DATA_PATH, 'r') as f:

            parser = csv.DictReader(f)
            for row in parser:
                row['total'] = int(row['total'])
                row['streak'] = int(row['streak'])
                row['max_streak'] = int(row['max_streak'])
                row['date_completed'] = int(row['date_completed'])
                task_list.append(row)
        return task_list
    else:
        print('Datafile not found, creating one at $HOME/.dailies')
        save_data([])
        return []

def clean_streaks(list):
    """Checks whether any streaks are stale, and resets counter to 0 if so."""
    for d in list:
        if TODAY_ORD - d['date_completed'] > 1:
            d['streak'] = 0
    return list

def parse_args(list):
    """Parses arguments from command line and invokes proper function."""
    arg_cnt = len(sys.argv) - 1
    if arg_cnt < 1 or arg_cnt > 2:
        print('ERROR: Incorrect number of arguments!')
        print_help()
    elif sys.argv[1] == 'add':
        if arg_cnt == 2:
            return add_task(sys.argv[2], list)
        else:
            print('ERROR: add requires an argument!')
    elif sys.argv[1] == 'complete':
        if arg_cnt == 2:
            for d in list:
                if d['name'] == sys.argv[2]:
                    d = complete_task(d)
        else:
            print('ERROR: complete requires an argument!')
    elif sys.argv[1] == 'rm':
        if arg_cnt == 2:
            return remove_task(sys.argv[2], list)
        else:
            print('ERROR: rm requires an argument!')
    elif sys.argv[1] == 'list':
        list_all(list)
    elif sys.argv[1] == 'today':
        list_today(list)
    elif sys.argv[1] == 'help':
        print_help()
    else:
        print('ERROR: Invalid command!')
        print_help()
    return list

def list_all(list):
    """Prints a table with tasks and stats."""
    print('{0:10} | {1:5} | {2:6} | {3:5}'.format('Task', 'Total', 'Streak', 'Max Streak'))
    for d in list:
        print('{0:10} | {1:5} | {2:6} | {3:5}'.format(d['name'], d['total'], d['streak'], d['max_streak']))

def list_today(list):
    """Prints a list of all tasks still due today"""
    print('TODO\n')
    for d in list:
        if d['date_completed'] == TODAY_ORD - 1:
            print(d['name'])

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
    return list

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
                #TODO rm n test fails
                break
            else:
                confirm = input('[y/n]?')
    else:
        print('ERROR: Task not found!')
    return list

def complete_task(task):
    """Adds one to the task's total, checks if a streak is occuring."""
    task['total'] += 1
    if task['date_completed'] != TODAY_ORD:
        task['streak'] += 1
    if task['streak'] > task['max_streak']:
        task['max_streak'] = task['streak']
    task['date_completed'] = TODAY_ORD
    return task

def print_help():
    """Prints list of commands with descriptions."""

    help_text = """Dailies
A simple command line utility for keeping track of daily tasks.

Commands:
    help    Print this text.
    add     Add a new daily.  Takes a task name argument.
    rm      Permenantly remove a daily.  Takes a task name argument.
    complete Mark a task complete.  Takes a task name argument.
    list    Display all dailies and their stats.
    today   Display all tasks due yet today."""

    print(help_text)

def save_data(list):
    """Writes list of dicts to file."""
    with open(DATA_PATH, 'w') as f:
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
    """Main body of dailies cli"""
    task_list = load_data()
    task_list = clean_streaks(task_list)
    task_list = parse_args(task_list)
    save_data(task_list)

main()
