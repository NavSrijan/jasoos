import os
import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ["DATABASE_URL"]

"""
CREATE TABLE "members" (
	"id" BIGINT NOT NULL,
	"name" TEXT NOT NULL,
	"age" TEXT,
	"sex" TEXT,
	"location" TEXT,
	"hobbies" TEXT,
	"indian" INT,
	PRIMARY KEY ("id")
);
"""


class Database():
    def __init__(self,DATABASE_URL,tableName):
        self.DATABASE_URL = DATABASE_URL
        self.tableName = tableName
    def connect(self):
        self.conn = psycopg2.connect(self.DATABASE_URL)
        return self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    def closeConnection(self):
        self.conn.commit()
        self.conn.close()
    
    def updateMember(self, person):
        sql = """UPDATE {}
        SET name=%s,
            age=%s,
            sex=%s,
            location=%s,
            hobbies=%s,
            indian=%s
        WHERE id=%s;
        """.format(self.tableName)
        cursor = self.connect()
        cursor.execute(sql,(person.name, person.age, person.sex, person.location, person.hobbies, person.indian, person.id))
        self.closeConnection()

    def addMember(self,person):
        try:
            cursor = self.connect()
            if person.indian:
                person.indian = 1
            else:
                person.indian = 0
            sql = """INSERT INTO {} (id, name, age, sex, location, hobbies, indian)
    VALUES  (%s, %s, %s, %s, %s, %s, %s);""".format(self.tableName)
            cursor.execute(sql,(person.id, person.name, person.age, person.sex, person.location, person.hobbies, person.indian))
            self.closeConnection()
        except Exception as e:
            if type(e)==psycopg2.errors.UniqueViolation:
                try:
                    self.closeConnection()
                    self.updateMember(person)
                except:
                    print("Exception in exception")
    def viewAllUsers(self):
        cursor = self.connect()
        cursor.execute("SELECT * from {};".format(self.tableName))
        temp = cursor.fetchall()
        self.closeConnection()
        return(temp)

def apppendMember(person):
    db = Database(DATABASE_URL, "members")
    db.addMember(person)
