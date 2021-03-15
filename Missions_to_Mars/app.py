from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/database_name")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():



if __name__ == "__main__":
    app.run(debug=True)