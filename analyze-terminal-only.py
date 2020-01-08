import os.path, time
import csv
import datetime

# Specify the original csv file to analyze
filename = "2020-01-06 Event Log ETPDLN [Submittable - F3].csv"


# TODO: add ability to specify a date range for analysis. This is needed because the keycard software doesn't let you export data by date (it only exports by number of records)


# Initialize our lists and counters for events we want to identify
rows = []
counterUserDeniedAccess = []
counterEntryAttemptDenied = []
counterTimeLate = []
counterTimeExtraLate = []
counterTempCardEvents = []
counterUniqueTempCards = []
datetimeList = []
earliestDateTime = []
latestDateTime = []

# Specify the events and users we are looking for
eventUserDeniedAccess = "User Denied Access"
eventEntryAttemptDenied = "Entry Attempt Denied"
userTempCard = "Temp Card"
timeLate = ["19", "20"] # this is suuuper janky, but whatev
timeExtraLate = ["21", "22", "23", "00", "01", "02", "03"] # more jankiness, but these are the hours of 9:00 pm through 3:59 am

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

    # Store rows that contain User Denied Access, but exclude Temp Install (admin) events
    for row in rows:
        if (eventUserDeniedAccess in row[4]) & (row[3] != ' Temp Install'):
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
        # Check the hour against the list of weird entry times and add only if the entry is NOT a system reserved date stamp
        for elem in timeLate:
            if (elem == new_time) & (row[4] != ' Reserved Date Stamp'):
                counterTimeLate.append(row)
        # Check the hour against the list of extra unusual entry times and add only if the entry is NOT a system reserved date stamp (which is only there to facilitate human reading the bare csv printout top to bottom)
        for elem in timeExtraLate:
            if (elem == new_time) & (row[4] != ' Reserved Date Stamp'):
                counterTimeExtraLate.append(row)       

    # Store Temp Card events
    for row in rows:
        if userTempCard in row[3]:
            counterTempCardEvents.append(row)
    
    # Store temp card numbers
    for elem in counterTempCardEvents:
        counterUniqueTempCards.append(elem[2])


    # Convert dates to datetime objects and store to list for min/max picking
    for row in rows:
        date = row[0]
        d = datetime.datetime.strptime(date, '%m/%d/%y')
        new_date = d.strftime('%m/%d/%y')
        datetimeList.append(new_date)
    
    # Store min and max of datetimeList into earliestDateTime and latestDateTime
    earliestDateTime = min(datetimeList)
    latestDateTime = max(datetimeList)


    # Log the results
    from datetime import datetime
    print("\n* * * * * * * Log Report Dated:", datetime.now(), "* * * * * * *")

    print("\nName of log file: ", os.path.basename("/Users/jamieiguchi/projects/python/keycards/2020-01-06 Event Log ETPDLN [Submittable - F3].csv"))
    
    print("\nThis log contains %d events"%(csvreader.line_num))

    print("\nLog date range:", earliestDateTime, "to", latestDateTime)

    print("\nSelected date range for this report:", ) #TODO - add date range

    print("\nThe temp cards used during this period were:", set(counterUniqueTempCards))

    print("\nThe number of events that occurred between 7:00 pm and 8:59 pm is: ", len(counterTimeLate))
    print("These events were:")
    for elem in counterTimeLate:
        print(elem)
    
    print("\nThe number of events that occurred between 9:00 pm and 3:59 am is: ", len(counterTimeExtraLate))
    print("These events were:")
    for elem in counterTimeExtraLate:
        print(elem)

    print("\nThe number of times an active, assigned card was denied access is: ", len(counterUserDeniedAccess))
    print("These events were:")
    for elem in counterUserDeniedAccess:
        print(elem)

    print("\nThe number of times an incorrect key code was entered is: ", len(counterEntryAttemptDenied))
    print("These events were:")
    for elem in counterEntryAttemptDenied:
        print(elem)

    print("\nThe number of times a temp card user gained access is: ", len(counterTempCardEvents))
    print("These events were:")
    for elem in counterTempCardEvents:
        print(elem)





# Specify a specific date you want to look at (optional)
# specialDate = '01/06/20'

    # print("\nThese are all events that occurred on the specified date: ")
    # for row in rows:
    #     if (row[0] == specialDate):
    #         print(row)