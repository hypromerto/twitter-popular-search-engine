from flask import Flask, request, render_template
import twitter
import json

app = Flask(__name__)

#Dummy account credentials
consumer_key = "HcsgBfYNZSnlNfgsbUnNHAGsi" 
consumer_secret = "22HO1U79YNChhmNz8Fbz6wUgQp5AiDCdhwodwehwSOJOXhWiu7"

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
      print(tweet['text'])
      resultDict[ tweet['user']['name']] = tweet['text']
      
   
   return json.dumps(resultDict)
   

if __name__ == '__main__':
   app.run(debug = True)