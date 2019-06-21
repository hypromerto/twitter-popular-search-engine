import mysql.connector, json

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="testdatabase123",
  database="twitter"
)

cursor = db.cursor() 


def insert_to_table(search_parameter, texts):
  
  tweet = json.dumps(texts)

  if not texts:
    tweet = None

  first = ("INSERT INTO results " "(search_parameter, tweets) " "VALUES (%s,%s)")
  cursor.execute(first,(search_parameter,tweet))

  db.commit()

def load_from_table(key):
  check = ("SELECT tweets " "FROM results " "WHERE EXISTS (SELECT search_parameter FROM results WHERE " "search_parameter = %s) AND search_parameter = %s")
  cursor.execute(check,(key,key,))

  for x in cursor:
    return x

