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

def data_collection():

    # Do data collection
    print("Great, let's begin the entry process:")
    print("First off, what's the first name of the person you're mad at?")
    name = input()
    print("And what did "+name+" do?")
    offence = input()
    print("And how many days do you want to be made at "+name+" for, given this greivous offence?")
    duration = integercheck()
    # Determine expiry date of anger based on current date and desired duration of anger
    exp = datetime.date.today() + datetime.timedelta(days = duration)
    #Enter data into Names table
    cur.execute('''INSERT OR IGNORE INTO Names (name) VALUES (?)''',(name,))
    #Get id for perp from Names table
    cur.execute('SELECT id From Names WHERE name = ? LIMIT 1',(name,))
    for row in cur:
        number = row[0]
    #Insert id, offence, and duration into Offence table
    cur.execute('INSERT INTO Offence (crime, perp, expiry) VALUES (?, ?, ?)',(offence, number, exp,))
    #Commit to the database before asking if there's a new grievance to deal with
    conn.commit()
    print("Was that you last new greivance (Y/N)")
    lg = input()
    while lg != "Y" and lg != "N" and lg != "y" and lg != "n":
        print("Please enter Y or N")
        lg = input()
    if lg == "Y" or lg =="y":
        print("OK, let's see if you have any old greivances still ongoing")
    # If there's another greivance to add recursively call data_collection()
    elif lg == "N" or lg =="n":
        data_collection()

# Create database if necessary and open cursor
conn = sqlite3.connect('angrydb.sqlite3')
cur = conn.cursor()

# # Destroy any exiting table (just for development testint)
# cur.execute('DROP TABLE IF EXISTS Offence')
# cur.execute('DROP TABLE IF EXISTS Names')

# # Creating the Offence table only if it doesn't already exist
cur.execute('CREATE TABLE IF NOT EXISTS Offence (crime TEXT, perp INTEGER, expiry TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS Names (id INTEGER NOT NULL PRIMARY KEY UNIQUE, name TEXT UNIQUE)')

print("Hello! Welcome to the Angry App!")
print("Would you like to enter a new greivance (Y/N)")
ng = input()
while ng != "Y" and ng != "N" and ng != "y" and ng != "n":
    print("Please enter Y or N")
    ng = input()
if ng=="Y" or ng=="y":
    data_collection()
elif ng=="N" or ng =="n":
    print("Smooth day at work, eh? Well, before you disappear let's just see if you're still mad at somebody for something done and past.")


cur.close()
