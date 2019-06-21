from flask import Flask, request, render_template
import twitter, redisCache, resultDB
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

   resultTexts, resultHashtags = redisCache.getCachedResults(search_parameter)
   
   if not resultTexts:
      tweet_data = twitter.fetchTweets(consumer_key, consumer_secret, search_parameter).json()
      texts = []
      hashDict = {}

      for tweet in tweet_data['statuses']:
         texts.append(tweet['text'])
         if tweet['entities']['hashtags']:
            for hashtag in tweet['entities']['hashtags']:
               hashtagText = hashtag['text']
               if hashtagText in hashDict:
                  hashDict[hashtagText] += 1
               else:
                  hashDict[hashtagText] = 1
            
      redisCache.cacheResults(search_parameter, texts, hashDict)
      resultDB.createTables(search_parameter, texts)

      # for key in hashDict:
      #    print(key + " : " + str(hashDict[key]))
      return json.dumps(texts)

   else:
      # for key in resultHashtags:
      #   print(key + " : " + str(resultHashtags[key]))
   return json.dumps(resultTexts)



if __name__ == '__main__':
   app.run(debug = True)