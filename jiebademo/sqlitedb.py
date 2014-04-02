import sqlite3
import domain

def createTextTable():
    createDb = sqlite3.connect('lemon_keyword.db', check_same_thread=False)
    createDb.text_factory = str
    queryCurs = createDb.cursor()
    queryCurs.execute('''CREATE TABLE texts
    (id INTEGER PRIMARY KEY, name TEXT, author TEXT, period TEXT, path TEXT, uploader TEXT, uploadDate TEXT, text Text)''')
    #queryCurs.execute('''CREATE TABLE uploadertexts
    #(textid INTEGER PRIMARY KEY, uploaderid INTEGER PRIMARY KEY)''')
    createDb.commit()
    queryCurs.close()
    createDb.close()

def createKeywordsTable():
    createDb = sqlite3.connect('/home/lanli/jiebademo/jiebademo/lemon_keyword.db', check_same_thread=False)
    createDb.text_factory = str
    queryCurs = createDb.cursor()
    queryCurs.execute('''CREATE TABLE keywords
    (id INTEGER PRIMARY KEY, textId INTEGER, name TEXT, count INTEGER, FOREIGN KEY (textId) REFERENCES texts(id))''')
    #queryCurs.execute('''CREATE TABLE uploadertexts
    #(textid INTEGER PRIMARY KEY, uploaderid INTEGER PRIMARY KEY)''')
    createDb.commit()
    queryCurs.close()
    createDb.close()

def addText(text):
    createDb = sqlite3.connect('lemon_keyword.db', check_same_thread=False)
    createDb.text_factory = str
    queryCurs = createDb.cursor()
    queryCurs.execute('''INSERT INTO texts (name,author,period,path,uploader,uploadDate,content)
    VALUES (?,?,?,?,?,datetime('now'),?)''',(text.name,text.author,text.period,text.path,text.uploader,text.content))
    createDb.commit()
    id = queryCurs.lastrowid
    queryCurs.close()
    createDb.close()
    return id

def addKeywords(keywords):
    createDb = sqlite3.connect('lemon_keyword.db', check_same_thread=False)
    createDb.text_factory = str
    queryCurs = createDb.cursor()
    for keyword in keywords:
        queryCurs.execute('''INSERT INTO keywords (name,count,textId)
        VALUES (?,?,?)''', (keyword.name, keyword.count, keyword.textId))
    createDb.commit()
    id = queryCurs.lastrowid
    queryCurs.close()
    createDb.close()
    return id

def getTexts():
    createDb = sqlite3.connect('lemon_keyword.db', check_same_thread=False)
    createDb.text_factory = str
    queryCurs = createDb.cursor()
    queryCurs.execute('SELECT id,name,author,period,path,uploader,uploadDate FROM texts ORDER BY uploadDate')
    texts = []
    for i in queryCurs:
        text = domain.Text(i[0],i[1],i[2],i[3],i[4],i[5],i[6],'')
        texts.append(text)
    queryCurs.close()
    createDb.close()
    return texts

def getText(id):
    createDb = sqlite3.connect('lemon_keyword.db', check_same_thread=False)
    createDb.text_factory = str
    queryCurs = createDb.cursor()
    queryCurs.execute("SELECT * FROM texts where id = '%s' ORDER BY uploadDate" % id)
    text = None
    for i in queryCurs:
        text = domain.Text(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])
        break
    queryCurs.close()
    createDb.close()
    return text

def deleteTexts(ids):
    createDb = sqlite3.connect('lemon_keyword.db', check_same_thread=False)
    queryCurs = createDb.cursor()
    queryCurs.execute("delete FROM texts where id in (%s)" % ', '.join(ids))
    queryCurs.execute("delete FROM keywords where textId in (%s)" % ', '.join(ids))
    createDb.commit()
    queryCurs.close()
    createDb.close()

def getKeywords(textId, topK):
    createDb = sqlite3.connect('lemon_keyword.db', check_same_thread=False)
    queryCurs = createDb.cursor()
    queryCurs = createDb.cursor()
    if(topK == -1):
        queryCurs.execute("SELECT name,count FROM keywords where textId = {0} ORDER BY count desc".format(textId))
    else:
        queryCurs.execute("SELECT name,count FROM keywords where textId = {0} ORDER BY count desc LIMIT {1}".format(textId, topK))
    keywords = []
    for i in queryCurs:
        keyword = domain.Keyword(id=0, name=i[0], count=i[1], textId=textId)
        keywords.append(keyword)
    queryCurs.close()
    createDb.close()
    return keywords

def main():
    createKeywordsTable()
    #print getTexts()
    #addCust('Derek Banas','5708 Highway Ave','Verona','PA',150.76)
    #addCust('Karl Tong','5708 Highway Ave','Verona','PA',250.76)

    #k = 0

    #for i in queryCurs:
        #print "\n"
        #for j in i:
            #print listTitle[k]
            #print j
            #if k < 5: k+=1
            #else: k=0

if __name__ == '__main__': main()