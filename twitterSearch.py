from flask import Flask, request, render_template
import json,requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('landing.html')

@app.route('/search', methods = ['POST'])
def search():
   req_data = request.get_json()
   search_parameter = req_data['search_parameter'] 

   requests.get('https://api.twitter.com/1.1/search/tweets.json',
               params={''}

)
   return search_parameter


if __name__ == '__main__':
   app.run(debug = True)