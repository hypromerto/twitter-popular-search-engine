from flask import Flask, request, render_template, jsonify, Response
import twitter, redis_cache, result_db, validator, json

app = Flask(__name__)

# Dummy account credentials
consumer_key = "HcsgBfYNZSnlNfgsbUnNHAGsi" 
consumer_secret = "22HO1U79YNChhmNz8Fbz6wUgQp5AiDCdhwodwehwSOJOXhWiu7"


@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/search', methods = ['POST'])
def search():
   '''
   Validate the input, respond 400 BAD REQUEST if the input is not validated.
   If it is, continue.
   '''
   body = validator.validate({
      "search_parameter": validator.field("search_key",required=True,minlength= 1, maxlength=100)
   }, request.get_json())

   if isinstance(body, Response): # 400 BAD REQUEST
      return body 
   
   search_parameter = body["search_parameter"]
   print("param:" + search_parameter)

   result_texts, result_hashtags = redis_cache.get_cached_results(search_parameter)
      
   if not result_texts:
      tweet_data = twitter.fetch_tweets(consumer_key, consumer_secret, search_parameter).json()
      texts = []
      hash_dict = {}

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

      return jsonify(texts)

   return jsonify(result_texts)



if __name__ == '__main__':
   app.run(debug = True)