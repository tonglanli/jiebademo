import sqlite3

createDb = sqlite3.connect(':memory:')

queryCurs = createDb.cursor()

def createTable():
    queryCurs.execute('''CREATE TABLE customers
    (id INTEGER PRIMARY KEY, name TEXT, street TEXT, city TEXT, state TEXT,balance REAL)''')

def addCust(name,street,city,state,balance):
    queryCurs.execute('''INSERT INTO customers (name,street,city,state,balance)
    VALUES (?,?,?,?,?)''',(name,street,city,state,balance))

def main():
    createTable()

    addCust('Derek Banas','5708 Highway Ave','Verona','PA',150.76)
    addCust('Karl Tong','5708 Highway Ave','Verona','PA',250.76)

    createDb.commit()

    queryCurs.execute('SELECT * FROM customers ORDER BY balance')

    listTitle = ['Id Num', 'Name','Street','City','State','Balance']
    k = 0

    for i in queryCurs:
        print "\n"
        for j in i:
            print listTitle[k]
            print j
            if k < 5: k+=1
            else: k=0
    queryCurs.close()

if __name__ == '__main__': main()