from flask import Flask, request, render_template
import twitter
import json

app = Flask(__name__)
consumer_key = "vZc6pCoCwPV7yhq5m29nhvtQ6"
consumer_secret = "igqixBkamWDVTsJlIwmt2S8Y2P0O1X0NeXKy4aroimT7Wr4NhC"

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/search', methods = ['POST'])
def search():
   req_data = request.get_json()
   search_parameter = req_data['search_parameter'] 
   result = twitter.fetchTweets(consumer_key, consumer_secret, search_parameter)
   
   tweet_data = result.json()

   resultDict = {}
   for tweet in tweet_data['statuses']:
      resultDict[ tweet['user']['name']] = tweet['text']

   return json.dumps(resultDict)
   

if __name__ == '__main__':
   app.run(debug = True)