import re
import csv
import datetime as dt
import sys


class App(object):
    """
Author: Gregory Covington
Date: 2/17/2017
Description:
Work log is term program to help prepare better timesheets for the company
It will log what work someone did on a certain day.
Asks for task name, how much time was spent on the task, general notes
about the task. It will record all of the items in a row of a .csv file along
with the date It will provide functionality for the user to find all the
tasks that were done on a certain date or that match a search string using
a regex or plain text.
It will print the report to the screen, including the
      DATE, TITLE, TIME_SPENT, and GENERAL NOTES
Task entries can be deleted or edited.  User can edit the task name, time
spent, date, and/or notes.
Entries are displayed one at a time and can be paged through one by one

    Attributes:
        lfile -- the file where the task records are stored in csv format
        tlist -- list of dictionaries representing the tasks read from the file
        slist -- pipe for sorted and searched list of tasks
        fnames -- static attribute holding the fieldnames for the tasks
        """
    lfile = 'log.csv'

    def __init__(self):
        self.today = dt.datetime.now().strftime("%m/%d/%Y")
        self.fnames = ['id','date', 'name', 'duration', 'notes']
        self.tlist = self.read_log()
        self.slist = self.tlist[:]
        self.index = 0
        self.current = self.slist[self.index]
        self.order = self.fnames[1]
        self.title = 'All tasks'
        self.main_loop()


    def main_loop(self):
        """The Program's main loop managing the screen printing and user interface.
            """

        title = 'All Tasks'
        while True:
            self.clear_screen()
            self.save_tlist()
            self.print_screen()
            cmd = input("\nEnter a command: ").strip().lower()

            if cmd[0] == 'a':
                self.add_task()
            elif cmd[0] == 'f':
                if int(cmd[1]) in range(5):
                    self.find(cmd[1], cmd[3:])
                elif int(cmd[1]) == 5:
                    self.rpattern(cmd[3:])
                else:
                    print("Try Again...")
                    return self.main_loop()
            elif cmd[0] == 'n':
                self.index +=1
                continue
            elif cmd[0] == 'p':
                self.index -= 1
                continue
            elif cmd[0] == 'e':
                self.edit_task(self.current["id"])
            elif cmd[0] == 'q':
                    self.clear_screen()
                    self.save_log()
                    print("Thank You for using Work Log!")
                    sys.exit(0)
            else:
                print("Try Again...")
                return self.main_loop

    def print_screen(self):
        print(
            " __      __                  __     .____\n"
            "/  \    /  \  ____  _______ |  | __ |    |      ____     ____  \n"
            "\   \/\/   / /  _ \ \_  __ \|  |/ / |    |     /  _ \   / ___\ \n"
            " \        / (  |_| ) |  | \/|    <  |    |___ (  |_| ) / /_/  |\n"
            "  \__/\__/   \____/  |__|   |__|__\ |________\ \____/  \___  / \n"
            "                                                      /_____/  \n"
            "\n"
            "Welcome to Work Log!\n"
            )
        print('--------------------------------------------------------------')
        print(
                "{0!s:^60} ".format("MENU :\n"
                ": a     -  Add a new task\n"
                ": p     -  (p)revious task\n"
                ": e     -  (e)dit task"
                ": n     -  (n)ext task\n"
                ": s     -  (s)elect current task by number"
                ": q     -  (q)uit\n"
                ": fn [term] -  Find by n where n is the search type\n"
                "               and term is the search term.\n"
                "\t\t 1 - date\t"
                "\t\t 2 - name\n"
                "\t\t 3 - duration\t"
                "\t\t 4 - notes\n"
                "\t\t 5 - regex pattern"
                )
        print('--------------------------------------------------------------')
        print(
            "Today's Date: {}\n".format(self.today) +
            "Working on {}".format(self.lfile)
            )
        print()
        self.print_tasks(self.title, self.order)
        self.current = self.slist[self.index]
        print(
                "-------------------------------------------------------------"
                "--------------------\n{5!s:^80}"
                "\n\tId: {4!s:>3}\n\t---------\n"
                "\tDate: {0!s:<20s}\n\tName: {1!s:<20s}\n\tDuration: {2!s:<20s}\n\tNotes: {3!s:<20s}".format(
                                                    self.current["date"],
                                                    self.current["name"],
                                                    self.current["duration"],
                                                    self.current["notes"],
                                                    self.current["id"],
                                                    'EDIT TASK'
                                                            )
                )

    def clear_screen(self):
        print("\033c", end="")

    def read_log(self):
        try:
            with open(self.lfile, 'x', errors='ignore') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fnames)
                writer.writeheader()
        except:
            with open(self.lfile, newline='') as csvfile:
                reader = csv.DictReader(csvfile, delimiter=',')
                return list(reader)

    def save_log(self):
        with open(self.lfile, 'r') as csvfile:
            task_writer = csv.DictWriter(csvfile, fieldnames=self.fnames)
            for task in self.tlist:
                task_writer.writerow(task)

    def add_task(self):
        attrs = (
                len(self.tlist) + 1,
                self.today,
                input("Enter task name:").strip(),
                input("Enter time spent in minutes:").strip(),
                input("Enter any notes:").strip()
                )
        self.tlist.append(map(self.fnames, attrs))

    def edit_task(self, id):
        while True:
            ask = int(input(
                "What would you like to edit?\n"
                "(1) date (2) name (3) duration (4) notes:  "
                ).strip().lower())
            choices = ['date', 'name', 'duration', 'notes']
            self.current[choices[ask]] = input("Enter new {} data:".format(choices[ask]))
            again = input("Would you like to change something else? (y,n)")
            self.clear_screen()
            self.print_screen()
            if again == 'y':
                self.edit_task()
            elif again == 'n':
                break
            else:
                print("failed")
                continue

    def find(self, stype, sterm):
        tasks = [t for t in self.tlist if t[self.fnames[int(stype)]] == sterm]
        if tasks:
            self.slist = tasks
        else:
            print('fail')

    def rpattern(self, pattern):
        pattern = re.compile(pattern)
        tasks = []
        with open("log.csv", encoding="utf-8") as logfile:
            for i, line in enumerate(logfile):
                if pattern.search(line):
                    tasks.append(i)
        self.slist = [t[x] for t in self.tlist for x in tasks]


    def save_tlist(self):
        self.tlist = [s if t['id'] == s['id'] else t for t in self.tlist for s in self.slist]

    def print_tasks(self, title, fname):
        tasks = self.order_by(fname)
        print("{0!s:^80s}\n".format(title)+"-"*80 + "\n")
        print("{:^25}    {:<15}{:<21}{:<20}".format(*self.fnames[1:]))
        count = 0
        for task in tasks:
            if count == self.index:
                print(" "+str(count)+") >>", end='')
            else:
                print(""+(str(count)+")  ").rjust(5), end='')
            print("\t{0!s:<20s}{1!s:<19s}{2!s:<14s}{3!s:<20s}".format(
                                                    task["date"],
                                                    task["name"],
                                                    task["duration"],
                                                    task["notes"]
                                                    ))
            count += 1
        print()

    def order_by(self, fname='date'):
        return sorted(self.slist, key=lambda k: k[fname], reverse=True)

if __name__ == '__main__':
    App()
# TODO
# Use named tuples instead of dicitonary
# use .replace(key=newvalue) for editing entries
# line = re.compile(regex)
# for match in line.finditer(data):
#   print(match.group)
