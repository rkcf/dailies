import sys 

task_list = []

# Check for data file in $HOME/.dailies.

# Create one if it does not exits.

# Load data to python data structures.
# name, times_completed, current_streak, max_streak, date_last_completed

# Cleanup Streaks
# Checks each tasks date_last_complete against current date, if it is two
# days previous, the current_streak is reset to 0.

# Parse Arguments.
def parse_args():
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

# List Command
# Print each daily task along with max completions and current streak to the
# terminal. Orderd by current streak.
def list_all():
    print ('{0:5} | {1:5}'.format('Task', 'Total'))
    for task in task_list:
        print ('{0:5} | {1:5d}'.format(task['name'], task['times_completed']))

# Today Command
# Print each task that needs to be done yet today.

# Add Command
# Accepts user input for new task name and adds it to list.
def add_task(name):
    task = {'name': name,
            'times_completed': 0,
           }
    task_list.append(task)

# Remove Command
# Prompts user to confirm, then removes task from list.
def remove_task(task):
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

# Complete Command
# Updates date_last_completed value of task to todays date.  Increments 
# times_completed.  Adds one to current_streak, and updates max_streak as
# needed.

# Help Command
# Prints command list
def print_help():
    print('help')


# Save changes

def main():
    parse_args()

main()
