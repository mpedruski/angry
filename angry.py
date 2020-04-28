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

def inputcheck():
    x = input()
    while x != "Y" and x != "y" and x != "N" and x != "n":
        print("Please enter Y or N")
        x = input()
    return(x)

def notnegative():
    x = integercheck()
    while x < 0:
        print("You can't be mad at someone for negative time! Give a positive integer!")
        x = integercheck()
    while x > 36500:
        print("OK, so that's a really long time... I'm gonna put you down for 100 years, but frankly, I doubt you can handle event that.")
        x = 36500
    return(x)

def data_collection(x):

    entries = x

    # Create database if necessary and open cursor
    conn = sqlite3.connect('angrydb.sqlite3')
    cur = conn.cursor()

    # # Creating the Offence table only if it doesn't already exist
    cur.execute('CREATE TABLE IF NOT EXISTS Offence (cid INTEGER NOT NULL PRIMARY KEY, crime TEXT, perp INTEGER, expiry TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS Names (pid INTEGER NOT NULL PRIMARY KEY UNIQUE, name TEXT UNIQUE)')

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
    print("\nAnd how many days do you want to be mad at "+name+" for, given this greivous offence?")
    duration = notnegative()
    # Determine expiry date of anger based on current date and desired duration of anger
    exp = datetime.date.today() + datetime.timedelta(days = duration)
    #Enter data into Names table
    cur.execute('''INSERT OR IGNORE INTO Names (name) VALUES (?)''',(name,))
    #Get id for perp from Names table so this can be added to the Offence table
    cur.execute('SELECT pid From Names WHERE name = ? LIMIT 1',(name,))
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
    lg = inputcheck()

    # If there's another greivance to add recursively call data_collection()
    if lg == "N" or lg =="n":
        data_collection(entries)

def data_report():
    # Create database if necessary and open cursor
    conn = sqlite3.connect('angrydb.sqlite3')
    cur = conn.cursor()
    cur.execute('''SELECT cid, name, crime, expiry FROM Offence JOIN Names ON Offence.perp=Names.pid WHERE expiry >= DATE('now') ORDER BY cid''')
    count = 0
    for row in cur:
        expdt = datetime.datetime.strptime(row[3],'%Y-%m-%d')
        expdt= datetime.datetime.strftime(expdt,'%b %d, %Y')
        output = "Greivance "+ str(row[0]) + ": " "You're mad at "+ row[1]+" until "+expdt+" for the following crime: "+row[2]
        print(output)
        count = count+1
    cur.close()
    if count >1:
        print("\nWow, you're carrying "+str(count)+" grudges. Maybe you should try taking it easier?")
    elif count == 1:
        print("\n1 grudge, eh? Not bad, but you could do better.")
    else:
        print("\n No grudges, that's what I like to see!")
    # Ask if any of the data about greivances needs to change
    if count > 0:
        print("\nDo you need to edit any of this data? (Y/N)")
        ed = inputcheck()
        if ed == "Y" or ed == "y":
            data_edit()

def data_edit():
    # Get information from user about what's going to change
    print("Please enter the number of the grievance you'd like to modify.")
    x = integercheck()
    print("OK, what aspect of the grievance would you like to modify? (Please enter one of the following numbers:)")
    print("\n 1) I'd need to change the name of the offender.")
    print("\n 2) I'd like to change the duration of the penalty.")
    print("\n 3) It turned out not to be a problem after all - delete the offence.")
    print("\n 4) Actually this data does look right!")
    y = integercheck()
    while y != 1 and y != 2 and y !=3 and y !=4:
        print("Please enter one of the options above.")
        y = integercheck()

    # # Create open cursor
    # conn = sqlite3.connect('angrydb.sqlite3')
    # cur = conn.cursor()

    if y == 1:
        print("\n Ok, what is the correct name of the offender?")
        new_name = input()
        # Create open cursor
        conn = sqlite3.connect('angrydb.sqlite3')
        cur = conn.cursor()
        cur.execute('''INSERT OR IGNORE INTO Names (name) VALUES (?)''',(new_name,))
        #Get pid for perp from Names table so this can be modified in the Offence table
        cur.execute('SELECT pid From Names WHERE name = ? LIMIT 1',(new_name,))
        new_numb = cur.fetchone()[0]
        cur.execute('UPDATE Offence SET perp = ? WHERE cid = ?',(new_numb, x, ))
        conn.commit()
        cur.close()


    elif y == 2:
        print("\n Ok, how many days should your anger last (from today)?")
        new_duration = notnegative()
        # Determine expiry date of anger based on current date and desired duration of anger
        new_exp = datetime.date.today() + datetime.timedelta(days = new_duration)
        # Create open cursor
        conn = sqlite3.connect('angrydb.sqlite3')
        cur = conn.cursor()
        cur.execute('UPDATE Offence SET expiry = ? WHERE cid = ?',(new_exp, x, ))
        conn.commit()
        cur.close()


    elif y == 3:
        print("\n Ok, we'll just delete that infraction altogether")
        conn = sqlite3.connect('angrydb.sqlite3')
        cur = conn.cursor()
        cur.execute('DELETE FROM Offence WHERE cid = ?',(x, ))
        conn.commit()
        cur.close()

    elif y ==4:
        print("\n Ok, no problem")

    print("\n Here's how the data looks now: \n")
    data_report()

if __name__ == '__main__':

    entries = 0
    # Getting input from user on whether there are greivances to enter, and whether they'd like a report
    print("Hello! Welcome to the Angry App!\n")
    print("Would you like to enter a new greivance (Y/N)")
    ng = inputcheck()
    # If they have a greivance initiate data_collection(), and regardless of their answer prompt them about a report
    if ng=="Y" or ng=="y":
        data_collection(entries)
        print("\nAwesome! Do you want to check on the list of things you're angry about (Y/N)?")
    elif ng=="N" or ng =="n":
        print("\nAwesome! Do you want to check on the list of things you're angry about (Y/N)?")
    ch = inputcheck()
    # If a report is wanted call data_report
    if ch=="Y" or ch=="y":
        print("\n")
        data_report()


    # At the end wish the user a good day
    print("\nGoodbye!")
