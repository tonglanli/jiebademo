import sqlite3
import domain

createDb = sqlite3.connect('/Users/mac/NLTK/jiebademo/jiebademo/lemon_keyword.db', check_same_thread=False)

queryCurs = createDb.cursor()

def createTable():
    queryCurs.execute('''CREATE TABLE texts
    (id INTEGER PRIMARY KEY, name TEXT, author TEXT, period TEXT, path TEXT, uploader TEXT, uploadDate TEXT)''')
    #queryCurs.execute('''CREATE TABLE uploadertexts
    #(textid INTEGER PRIMARY KEY, uploaderid INTEGER PRIMARY KEY)''')

def addText(name,author,period,path,uploader):
    queryCurs.execute('''INSERT INTO texts (name,author,period,path,uploader,uploadDate)
    VALUES (?,?,?,?,?,datetime('now'))''',(name,author,period,path,uploader))
    createDb.commit()

def getTexts():
    queryCurs.execute('SELECT * FROM texts ORDER BY uploadDate')
    texts = []
    for i in queryCurs:
        text = domain.Text(i[0],i[1],i[2],i[3],i[4],i[5],i[6])
        texts.append(text)
    return texts

def main():
    createTable()

    #addCust('Derek Banas','5708 Highway Ave','Verona','PA',150.76)
    #addCust('Karl Tong','5708 Highway Ave','Verona','PA',250.76)

    createDb.commit()

    #queryCurs.execute('SELECT * FROM customers ORDER BY balance')

    #listTitle = ['Id Num', 'Name','Street','City','State','Balance']
    #k = 0

    #for i in queryCurs:
        #print "\n"
        #for j in i:
            #print listTitle[k]
            #print j
            #if k < 5: k+=1
            #else: k=0
    queryCurs.close()

if __name__ == '__main__': main()