import os
from flask import Flask, render_template, jsonify, redirect
import pymongo
from bson.objectid import ObjectId
import scrape_mars

app = Flask(__name__)

dbuser = os.environ.get('dbuser')
dbpassword = os.environ.get('dbpassword')
conn = f"mongodb://{dbuser}:{dbpassword}@ds121950.mlab.com:21950/heroku_hj8l92mg"
client = pymongo.MongoClient(conn)
db = client.heroku_hj8l92mg
collection = db.mars


@app.route('/')
def index():
    mars = db.collection.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = db.collection
    mars_data = scrape_mars.scrape()
    mars.update_one(
        {'_id': ObjectId('5af9f2878cda9dbac35711e7')},
        {'$set': mars_data},
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=False)
