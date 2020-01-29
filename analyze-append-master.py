import os.path, time
import csv
import datetime

# Specify the original csv file to analyze and its path
LOG_FILE = "<YOUR FILE NAME>.csv"
LOG_FILE_PATH = "<YOUR PATH HERE>"

# Specify desired date range to anlayze, since the key card manufacturer's software does not allow for exporting logs by date (it only lets us export by number of records)
FROM_DATE = "<YOUR START DATE>"
TO_DATE = "<YOUR END DATE>"

# Specify the events and users we are looking for
USER_DENIED_ACCESS = "User Denied Access"
ENTRY_ATTEMPT_DENIED = "Entry Attempt Denied"
TEMP_CARD = "Temp Card"
LATE_TIME = ["19", "20"] # this is suuuper janky, but whatev
VERY_LATE_TIME = ["21", "22", "23", "00", "01", "02", "03"] # more jankiness, but these are the hours of 9:00 pm through 3:59 am

# Initialize our lists and counters for events we want to identify
rows = []
known_users_denied = []
unknown_persons_denied = []
late_entries = [] #for events occurring from 7:00 pm to 8:59 pm
very_late_entries = [] #for events occurring from 9:00 p m to 3:59 am
temp_card_events = []
temp_cards_used = []

# Read the csv file and log results
with open(LOG_FILE, 'r') as csvfile:

    # Create a csv reader object
    csvreader = csv.reader(csvfile, delimiter=',')

    # Skip first row of CSV file because we don't to catch header names for values
    next(csvreader)

    # Extract each data row, one by one
    for row in csvreader:
        from datetime import date
        date = row[0]
        d = datetime.datetime.strptime(date, "%m/%d/%y")
        if (date >= FROM_DATE) & (date <= TO_DATE):
            rows.append(row)

    # Store rows that contain User Denied Access, but exclude Temp Install (admin) events
    for row in rows:
        if (USER_DENIED_ACCESS in row[4]) & (row[3] != ' Temp Install'):
            known_users_denied.append(row)

    # Store rows that contain Entry Attempt Denied
    for row in rows:
        if ENTRY_ATTEMPT_DENIED in row[4]:
            unknown_persons_denied.append(row)

    # Store rows that contain entries outside of work hours
    for row in rows:
        from datetime import date
        # First convert HH:MM:SS XM format to 24 hour format
        time = row[1]
        d = datetime.datetime.strptime(time, ' %I:%M:%S %p')
        # Pick out the only piece we care about, which is the hour
        new_time = d.strftime('%H')
        # Check the hour against the list of weird entry times and add only if the entry is NOT a system reserved date stamp
        for elem in LATE_TIME:
            if (elem == new_time) & (row[4] != ' Reserved Date Stamp'):
                late_entries.append(row)
        # Check the hour against the list of extra unusual entry times and add only if the entry is NOT a system reserved date stamp (which is only there to facilitate human reading the bare csv printout top to bottom)
        for elem in VERY_LATE_TIME:
            if (elem == new_time) & (row[4] != ' Reserved Date Stamp'):
                very_late_entries.append(row)       

    # Store Temp Card events
    for row in rows:
        if TEMP_CARD in row[3]:
            temp_card_events.append(row)
    
    # Store temp card numbers
    for elem in temp_card_events:
        temp_cards_used.append(elem[2])


    # Write all results to master log text file

    f = open("master-log.txt", "a")

    from datetime import datetime
    print("\n* * * * * * * Log Report Dated:", datetime.now(), "* * * * * * *", file=f)

    print("\nName of log file: ", os.path.basename(LOG_FILE_PATH), file=f)

    print("\nSelected date range:", FROM_DATE, "to", TO_DATE, file=f)

       print("\nThis date range contains", len(rows), "events", file=f)

    print("\nThe temp cards used during this period were:", set(temp_cards_used), file=f)

    print("\nThe number of events that occurred between 7:00 pm and 8:59 pm is: ", len(late_entries), file=f)
    if len(late_entries) > 0:
        print("These events were:", file=f)
    for elem in late_entries:
        print(elem, file=f)
    
    print("\nThe number of events that occurred between 9:00 pm and 3:59 am is: ", len(very_late_entries), file=f)
    if len(very_late_entries) > 0:
        print("These events were:", file=f)
    for elem in very_late_entries:
        print(elem, file=f)

    print("\nThe number of times an active, assigned card was denied access is: ", len(known_users_denied), file=f)
    if len(known_users_denied) > 0:
        print("These events were:", file=f)
    for elem in known_users_denied:
        print(elem, file=f)

    print("\nThe number of times an incorrect key code was entered is: ", len(unknown_persons_denied), file=f)
    if len(unknown_persons_denied) > 0:
        print("These events were:", file=f)
    for elem in unknown_persons_denied:
        print(elem, file=f)

    print("\nThe number of times a temp card user gained access is: ", len(temp_card_events), file=f)
    if len(temp_card_events) > 0:
        print("These events were:", file=f)
    for elem in temp_card_events:
        print(elem, file=f)

    f.close()