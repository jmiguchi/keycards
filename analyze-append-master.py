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

    # Write (append) all results below to the master log

    f = open("master-log.txt", "a")

    from datetime import datetime
    print("\n* * * * * * * Log Analysis Dated:", datetime.now(), "* * * * * * *", file=f)

    print("\nName of log file: ", os.path.basename("/Users/jamieiguchi/projects/python/keycards/sample-event-log.csv"), file=f) # your file path goes here
    
    print("\nThis log contains %d events"%(csvreader.line_num), file=f)

    # TODO: Add date range by picking earliest and latest dates from CSV file to report
    print("\nEvent date range: ", file=f)


    print("\nThe number of times a user was denied access is: ", len(counterUserDeniedAccess), file=f)
    for elem in counterUserDeniedAccess:
        print(elem, file=f)

    print("\nThe number of times an entry attempt was denied is: ", len(counterEntryAttemptDenied), file=f)
    for elem in counterEntryAttemptDenied:
        print(elem, file=f)
    
    print("\nThe number of access events outside of business hours is: ", len(counterOutsideBusinessHours), file=f)
    for elem in counterOutsideBusinessHours:
        print(elem, file=f)
    
    print("\nThe number of times a temp card user gained access is: ", len(counterTempCardUsers), file=f)
    for elem in counterTempCardUsers:
        print(elem, file=f)
    
    print("\n\n", file=f)

    f.close()