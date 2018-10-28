# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 16:51:34 2018

@author: antho
"""

# import necessary libraries
from flask import Flask, render_template, jsonify
import pymongo
import scrape

# create instance of Flask app
app = Flask(__name__)

# create mongo connection
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_data_entries

#db = client.store_inventory

@app.route("/")
def home():
    """
    result_set = [{"Test":"This is a Test 0"}
                ,{"Test":"This is a Test 1"}
                ,{"Test":"This is a Test 2"}
                ,{"Test":"This is a Test 3"}]
    return jsonify(result_set)
    """
    
    
    
    """
    # @TODO: write a statement that finds all the items in the db and sets it to a variable
    # CODE GOES HERE
    # Store the entire team collection in a list
    products = list(db.produce.find())
    print(products)

    # Return the template with the teams list passed in
    return render_template('index.html', products=products)
    # @TODO: render an index.html template and pass it the data you retrieved from the database
    """
    mars_data = list(db.collection.find())[0]
    #return  render_template('index_test.html', mars_data=mars_data)
    return  render_template('index.html', mars_data=mars_data)

@app.route("/scrape")
def web_scrape():
    db.collection.remove({})
    mars_data = scrape.scrape_mars()
    db.collection.insert_one(mars_data)
    
    #return render_template("scrape_test.html")
    return render_template("scrape.html")

if __name__ == "__main__":
    app.run(debug=True)