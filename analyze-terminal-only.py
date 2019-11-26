import os.path, time
import csv
import datetime

# Specify the csv file to analyze
filename = "sample-event-log.csv"

# Initialize our lists and counters for events we want to identify
fields = [] 
rows = []
counterUserDeniedAccess = []
counterEntryAttemptDenied = []
counterOutsideBusinessHours = []
counterTempCardUsers = []

# Specify the events and users we are looking for
eventUserDeniedAccess = "User Denied Access"
eventEntryAttemptDenied = "Entry Attempt Denied"
userTempCard = "Temp Card"
timeOutsideBusinessHours = ["20", "21", "22", "23", "00", "01", "02", "03", "04", "05", "06"] # this is suuuper janky, but whatev

# Initialize new file to be created
f = open("newfile.txt", "a+")

# Read the csv file and log results
with open(filename, 'r') as csvfile:

    # Create a csv reader object
    csvreader = csv.reader(csvfile, delimiter=',')

    # Skip first row of CSV file because we don't to catch header names for values
    next(csvreader)

    # Extract each data row, one by one
    for row in csvreader:
        rows.append(row)

    # Store rows that contain User Denied Access
    for row in rows:
        if eventUserDeniedAccess in row[4]:
            counterUserDeniedAccess.append(row)

    # Store rows that contain Entry Attempt Denied
    for row in rows:
        if eventEntryAttemptDenied in row[4]:
            counterEntryAttemptDenied.append(row)

    # Store rows that contain entries outside of work hours
    for row in rows:
        from datetime import date
        # First convert HH:MM:SS XM format to 24 hour format
        time = row[1]
        d = datetime.datetime.strptime(time, ' %I:%M:%S %p')
        # Pick out the only piece we care about, which is the hour
        new_time = d.strftime('%H')
        # Check the hour against the list of weird entry times
        for elem in timeOutsideBusinessHours:
            if elem == new_time:
                counterOutsideBusinessHours.append(row)

    # Store Temp Card events
    for row in rows:
        if userTempCard in row[3]:
            counterTempCardUsers.append(row)

    # Log the results
    from datetime import datetime
    print("\n* * * * * * * Log Analysis Dated:", datetime.now(), "* * * * * * *")

    print("\nName of log file: ", os.path.basename("/Users/jamieiguchi/projects/python/keycards/event-log.csv"))
    
    print("\nThis log contains %d events"%(csvreader.line_num))

    print("\nThe number of times a user was denied access is: ", len(counterUserDeniedAccess))
    for elem in counterUserDeniedAccess:
        print(elem)

    print("\nThe number of times an entry attempt was denied is: ", len(counterEntryAttemptDenied))
    for elem in counterEntryAttemptDenied:
        print(elem)
    
    print("\nThe number of access events outside of business hours is: ", len(counterOutsideBusinessHours))
    for elem in counterOutsideBusinessHours:
        print(elem)
    
    print("\nThe number of times a temp card user gained access is: ", len(counterTempCardUsers))
    for elem in counterTempCardUsers:
        print(elem)