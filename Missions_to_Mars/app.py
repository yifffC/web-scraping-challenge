from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_data")

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    marsdata = mongo.db.marsinfo.find_one()
    return render_template("index.html", marsdata=marsdata)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    marsinfo = mongo.db.marsinfo
    marsscrapedata = scrape_mars.scrape()
    marsinfo.update({}, marsscrapedata, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)