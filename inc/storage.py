import mysql.connector

class Storage:
    def __init__(self):
        self.config = {
            'user': 'root',
            'password': 'root',
            'host': '127.0.0.1',
            'database': 'crawler',
            'raise_on_warnings': True
        }
        self.cnx = mysql.connector.connect(**self.config)
        self.cursor = self.cnx.cursor()

    def save(self,url):
        if self.isInStorage(url) == False :
            sql = "INSERT INTO indexes (url) VALUES ('"+url+"')"
            self.cursor.execute(sql)
            self.cnx.commit()
    
    def isInStorage(self,url):
        sql = "select url from indexes where url='"+url+"'"
        self.cursor.execute(sql)
        myresult = self.cursor.fetchall()
        print(len(myresult))
        if len(myresult) == 0:
            return False
        return True