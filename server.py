from flask import Flask, render_template, request, redirect, jsonify
from pymongo import MongoClient

import HN_Scraping
import dogvision
from HN_Scraping import hn

app = Flask(__name__)

cluster = MongoClient(
    'mongodb+srv://admin:admin@cluster0.xzjm3.mongodb.net/portfolio?retryWrites=true&w=majority')  # mongodb connection string
db = cluster.get_database('portfolio')
collection = db.messages


@app.route('/')
def my_home():
    return render_template('index.html')


@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)


def count_id():
    index = 0
    while True:
        yield index
        index += 1


@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        data = {
            'Email': request.form['email'],
            'Subject': request.form['subject'],
            'message': request.form['message']
        }
        collection.insert_one(data)

        return render_template('/thankyou.html')
    else:
        return 'something went wrong. Try again!!'


# to grab the input data and pass it to the import_links function
@app.route('/webscraper.html', methods=['POST'])
def get_input():
    inp = request.form['input']
    HN_Scraping.import_links(inp)
    result = HN_Scraping.sorted_hn(hn_list=hn)

    return render_template('scrape.html', result=result)


# get input data and predict on that
@app.route('/make_prediction', methods=['GET', 'POST'])
def make_prediction():
    breed = None
    letters = ['a', 'e', 'i', 'o', 'u']
    prediction_score = None

    if request.method == 'POST':
        if request.files:
            inp = request.files['image'].read()
            prediction = dogvision.make_predictions(inp)
            breed = prediction[0]

            if breed[0] in letters:
                breed = f"It's an {breed}"

            breed = f"It's a {breed}"
            prediction_score = f"I'm {int(prediction[1] * 100)} % sure of it"

    return render_template('dogbreed.html', breed=breed, prediction_score=prediction_score)