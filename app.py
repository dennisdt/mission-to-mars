from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars
collection = db.mars


@app.route('/')
def index():
    mars = db.collection.find_one()
    return render_template('index.html', mars=mars)


@app.route('/scrape')
def scrape():
    mars = db.collection
    mars_data = scrape_mars.scrape()
    mars.update(
        {},
        mars_data,
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
