import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Galata-25",
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS db")
cursor.execute("USE db")
cursor.execute("SET NAMES utf8mb4")
cursor.execute("ALTER DATABASE db CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci")

def createTables(search_parameter, texts):

    '''
        This implementation does not expire the rows
        of the table, which is useful if we want to
        keep an archive of popular tweets. This is
        not the case in caching, because the time
        it takes for the cache to expire is small,
        which makes it unlikely that the popularity
        of tweets for a given keyword changes in that
        time interval. In MySQL database, we are not
        concerned with the up-to-dateness of the 
        popularity of the resulting tweets.'''

    cursor.execute("CREATE TABLE IF NOT EXISTS " + search_parameter
                   + " (id INT AUTO_INCREMENT PRIMARY KEY, tweet VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL)")

    for item in texts:
        cursor.execute("INSERT INTO " + search_parameter + " (tweet) VALUES (%s)", (item,))

    db.commit()
    cursor.execute("SELECT * FROM " + search_parameter)

    for x in cursor:
        print("ID: " + str(x[0]) )
        print("Text: " + x[1])




