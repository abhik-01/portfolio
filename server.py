from flask import Flask, render_template, request
from pymongo import MongoClient
import HN_Scraping
from HN_Scraping import hn

app = Flask(__name__)

cluster = MongoClient('mongodb+srv://admin:admin@cluster0.xzjm3.mongodb.net/portfolio?retryWrites=true&w=majority')  # mongodb connection string
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
