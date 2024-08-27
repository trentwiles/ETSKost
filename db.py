import sqlite3, time
# dummy

connection = sqlite3.connect("db.db")

def create():
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS drinks (uniqueName TEXT, url TEXT)")
    connection.commit()
    cursor.execute("CREATE TABLE IF NOT EXISTS prices (uniqueName TEXT, price REAL, ml INTEGER, mlDollar REAL, costPerShot REAL, ts INTEGER)")
    connection.commit()
    print("Initialized database")
    return

create()

def insertNewDrink(name:str, url:str):
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    
    # check if the drink doesn't exist first
    s = selectDrink(name)
    if len(s) > 0:
        print("didn't insert, drink exists...")
        return False
    
    data = (name, url)
    cursor.execute("INSERT INTO drinks VALUES (?, ?)", data)
    connection.commit()
    return True

def insertNewPrice(name:str, price, ml, mlDollar, costPerShot):
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    data = (name, price, ml, mlDollar, costPerShot, round(time.time()))
    cursor.execute("INSERT INTO prices VALUES (?, ?, ?, ?, ?, ?)", data)
    connection.commit()
    return True

def selectAll():
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    return cursor.execute("SELECT * FROM drinks").fetchall()

def selectDrink(name):
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    data = (name,)
    return cursor.execute("SELECT * FROM drinks WHERE uniqueName=?", data).fetchall()

def selectAllPricesForDrink(name):
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    data = (name,)
    return cursor.execute("SELECT * FROM prices WHERE uniqueName=? ORDER BY ts DESC LIMIT 5", data).fetchall()

def wipeDrinks():
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    data = ()
    cursor.execute("DELETE FROM drinks WHERE 1=1", data)
    connection.commit()
    return

def wipePrices():
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    data = ()
    cursor.execute("DELETE FROM prices WHERE 1=1", data)
    connection.commit()
    return

def wipeAll():
    wipeDrinks()
    wipePrices()
    return

def wipeCertainPrice(name):
    connection = sqlite3.connect("db.db")
    cursor = connection.cursor()
    data = (name)
    cursor.execute("DELETE FROM prices WHERE uniqueName=?", data)
    connection.commit()
    return