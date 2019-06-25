from flask import Flask, request, render_template, jsonify, Response
from flask_cors import CORS
import twitter, redis_cache, result_db, validator, json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# Dummy account credentials
consumer_key = "HcsgBfYNZSnlNfgsbUnNHAGsi" 
consumer_secret = "22HO1U79YNChhmNz8Fbz6wUgQp5AiDCdhwodwehwSOJOXhWiu7"


@app.route('/search', methods = ['POST'])
def search():

   input = {
      "search_parameter": request.get_json(force = True)["search_parameter"]
   }
   print(input["search_parameter"])
   ''' 
   Validate the input, respond 400 BAD REQUEST if the input is not validated.
   If it is, continue.
   '''
   body = validator.validate({
      "search_parameter": validator.field("search_key",required=True,minlength= 1, maxlength=100)
   }, input)

   if isinstance(body, Response): # 400 BAD REQUEST
      return body 
   
   search_parameter = body["search_parameter"]

   '''
   First check cache for the keyword.
   '''
   result_texts, result_hashtags = redis_cache.get_cached_results(search_parameter)
   if not result_texts:

      '''
      If the keyword is not found in cache, check database.
      '''
      db_list = result_db.load_from_table(search_parameter) 
      if db_list is not None:
         if ( db_list[0] is None):
            result = {
               "texts": [],
               "hastags": {}
            }
            return jsonify("[]")
         result = {
            "texts": db_list[0],
            "hashtags": {}
         }
         print("returned from db")
         return jsonify(result)

      '''
      If the keyword is not on both cache and database, get it from Twitter.
      '''   

      tweet_data = twitter.fetch_tweets(consumer_key, consumer_secret, search_parameter).json()
      texts = []
      hash_dict = {}

      '''
      Extracting all of the resulting tweets.
      '''
      for tweet in tweet_data['statuses']:
         texts.append(tweet['text'])
         if tweet['entities']['hashtags']:
            for hashtag in tweet['entities']['hashtags']:
               hashtag_text = hashtag['text']
               if hashtag_text in hash_dict:
                  hash_dict[hashtag_text] += 1
               else:
                  hash_dict[hashtag_text] = 1
      redis_cache.cache_results(search_parameter, texts, hash_dict)
      result_db.insert_to_table(search_parameter, texts)


      if ( texts ):
         result ={
            "texts": texts,
            "hashtags": hash_dict
         }
         print("returned from twitter")
         return jsonify(result)
      result = {
         "texts": [],
         "hashtags": {}
      }
      print("returned from twitter no result")

      return jsonify(result)

   
   
   result = {
      "texts": result_texts,
      "hashtags": result_hashtags
   }
   print("returned from cache")

   return jsonify(result)



if __name__ == '__main__':
   app.run(debug = True)