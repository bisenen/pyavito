import urllib2
import sqlite3
import time

db_filename = '/tmp/avito.db'

query="wii"
url="https://www.avito.ru/moskva/igry_pristavki_i_programmy/igrovye_pristavki?view=list&q={0}".format(query)
host="https://www.avito.ru"



def exsql(query):
    with sqlite3.connect(db_filename) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def isSQLite3(filename):
    from os.path import isfile, getsize

    if not isfile(filename):
        return False
    if getsize(filename) < 100: # SQLite database file header is 100 bytes
        return False
    else:
        fd = open(filename, 'rb')
        Header = fd.read(100)
        fd.close()

        if Header[0:16] == 'SQLite format 3\000':
            return True
        else:
            return False

def init_exist_db():
    if isSQLite3(db_filename):
        pass
    else:
        query="""create table list (
                 id integer primary key autoincrement,
                 name text,
                 price int
                 );
                 """
        exsql(query)




def get(url1):
    #print url1
    a = urllib2.urlopen(url1)
    if a.code == 200:
        return a.read()
    else:
        print "can't get info from avito"
        raise IOError




def getItem(data):
    time.sleep(5)
    list = data.split('<div id="yandex-direct-org"> <script>')[0].split('<div class="item ')
    if len(list) != 0:
        for i in list:
            if "price" in i:
                try:
                    item_url = host + i.split("\n")[5].split(" ")[3].replace('href="',"").replace('"',"")
                    item_price = i.split("price")[1].split("</p>")[0].split("\n")[1].replace("&nbsp;","").split("&#160")[0].strip()
                    #print "insert"
                    exsql("INSERT INTO list (name,price) VALUES ('{0}','{1}');".format(item_url, item_price))
                except IndexError:
                    #print "indexerr"
                    pass
    else:
       print len(list)
       raise IOError
       pass



exsql('DELETE FROM list;')
init_exist_db()
for x in range(1,10):
    try:
        getItem(get(url+"&p={0}".format(x)))
        print x
    except IOError:
        break





for i in exsql("SELECT price,name FROM list where price > 2000 and price < 4000 ORDER BY price;"):
    print i
#for i in range(1,999)
#    url + "&p={0}".format()