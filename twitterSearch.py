from flask import Flask, request, render_template
import twitter, redisCache
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

   result = redisCache.getCachedResults(search_parameter)
   if not result:
      result = twitter.fetchTweets(consumer_key, consumer_secret, search_parameter)
      tweet_data = result.json()

      resultDict = {}
      for tweet in tweet_data['statuses']:
         resultDict[ tweet['user']['name']] = tweet['text']
      print(resultDict)
      redisCache.cacheResults(search_parameter, resultDict)

      return json.dumps(resultDict)
   else:
      return json.dumps(result)

   '''
   
      
   return json.dumps(resultDict)
   '''

if __name__ == '__main__':
   app.run(debug = True)