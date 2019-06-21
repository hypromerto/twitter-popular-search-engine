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
  print(tweet)
  print(type(tweet))
  test = "mert'aslan'"
  cursor.execute("INSERT INTO `results` (`search_parameter`, `tweets`) VALUES ('%s','%s');" % (search_parameter,test) )
  db.commit()





