import sqlite3
import datetime

def integercheck():
    x = input()
    try:
        y = int(x)
        return y
    except:
        print("Please enter your answer as an integer")
        return integercheck()

def data_collection(x):

    entries = x

    # Create database if necessary and open cursor
    conn = sqlite3.connect('angrydb.sqlite3')
    cur = conn.cursor()

    # # Creating the Offence table only if it doesn't already exist
    cur.execute('CREATE TABLE IF NOT EXISTS Offence (crime TEXT, perp INTEGER, expiry TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS Names (id INTEGER NOT NULL PRIMARY KEY UNIQUE, name TEXT UNIQUE)')

    # Greet the user appropriately
    if entries==0:
        print("\nGreat, let's begin the entry process:")
    else:
        print("\nOK, ready for the next entry:")

    # Collect data from the user for one particular offence
    print("\nWhat's the first name of the person you're mad at?")
    name = input()
    print("\nAnd what did "+name+" do?")
    offence = input()
    print("\nAnd how many days do you want to be made at "+name+" for, given this greivous offence?")
    duration = integercheck()
    # Determine expiry date of anger based on current date and desired duration of anger
    exp = datetime.date.today() + datetime.timedelta(days = duration)
    #Enter data into Names table
    cur.execute('''INSERT OR IGNORE INTO Names (name) VALUES (?)''',(name,))
    #Get id for perp from Names table so this can be added to the Offence table
    cur.execute('SELECT id From Names WHERE name = ? LIMIT 1',(name,))
    for row in cur:
        number = row[0]
    #Insert id, offence, and duration into Offence table
    cur.execute('INSERT INTO Offence (crime, perp, expiry) VALUES (?, ?, ?)',(offence, number, exp,))
    #Commit to the database, close the cursor, and update number of entries before asking if there's a new grievance to deal with
    conn.commit()
    cur.close()
    entries=entries+1

    # Determine if that was the last greivance to enter
    print("\nWas that you last new greivance (Y/N)")
    lg = input()
    while lg != "Y" and lg != "N" and lg != "y" and lg != "n":
        print("Please enter Y or N")
        lg = input()

    # If there's another greivance to add recursively call data_collection()
    if lg == "N" or lg =="n":
        data_collection(entries)

def data_report():
    # Create database if necessary and open cursor
    conn = sqlite3.connect('angrydb.sqlite3')
    cur = conn.cursor()
    cur.execute('''SELECT name, crime, expiry FROM Offence JOIN Names ON Offence.perp=Names.id WHERE expiry >= DATE('now') ORDER BY expiry''')
    count = 0
    for row in cur:
        expdt = datetime.datetime.strptime(row[2],'%Y-%m-%d')
        expdt= datetime.datetime.strftime(expdt,'%b %d, %Y')
        output = "\nYou're mad at "+ row[0]+" until "+expdt+" for the following crime: "+row[1]
        print(output)
        count = count+1
    if count >1:
        print("\nWow, you're carrying "+str(count)+" grudges. Maybe you should try taking it easier?")
    elif count == 1:
        print("\n1 grudge, eh? Not bad, but you could do better.")
    else:
        print("No grudges, that's what I like to see!")
    cur.close()

entries = 0
# Getting input from user on whether there are greivances to enter, and whether they'd like a report
print("Hello! Welcome to the Angry App!\n")
print("Would you like to enter a new greivance (Y/N)")
ng = input()
while ng != "Y" and ng != "N" and ng != "y" and ng != "n":
    print("Please enter Y or N")
    ng = input()
# If they have a greivance initiate data_collection(), and regardless of their answer prompt them about a report
if ng=="Y" or ng=="y":
    data_collection(entries)
    print("\nAwesome! Do you check on the list of things you're angry about (Y/N)?")
elif ng=="N" or ng =="n":
    print("\nAwesome! Do you check on the list of things you're angry about (Y/N)?")
ch = input()
while ch != "Y" and ch != "N" and ch != "y" and ch != "n":
    print("Please enter Y or N")
    ch = input()
# If a report is wanted call data_report
if ch=="Y" or ch=="y":
    data_report()

# At the end wish the user a good day
print("\nGoodbye!")
