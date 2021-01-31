from flask import Flask, flash, redirect, render_template, request, session, abort
import config
import string
import random
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from jinja2 import escape, Markup
import requests
from flask_cors import CORS
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')
    

@app.route("/createList", methods = ['POST'])
def createList():
    listName = request.form['name']  
    movies = []
    randID = str(''.join((random.choice(string.ascii_letters + string.digits) for i in range(10))))
    config.listings.insert_one({"id":randID, "name":listName, "movies":movies})
    message = "Your list has been created! Go to http://127.0.0.1:5000/" + randID + " to view your list."
    return render_template('index.html',message=message)
    
    
@app.route("/<ID>")
def viewList(ID):
    if(str(config.listings.find_one({"id":ID})) == "None"):
        error = "Sorry. Page not found. Try creating a new list."
        return render_template('index.html', error=error), 404 
    data = config.listings.find_one({"id":ID})
    listName = str(data["name"])
    movies = data["movies"]
    file = open("static/movieList.txt", "r")
    allTitles = file.readlines()
    file.close()
    print(allTitles)
    return render_template('watchlist.html', listName=listName, movies=movies, ID=ID, allTitles=allTitles)
    
    
@app.route('/addToList', methods = ['POST']) 
def addToList():
    ID = request.form['id'] 
    movieTitle = request.form['title']
    data = config.listings.find_one({"id":ID})
    listName = data["name"]
    movies = data["movies"]
    movies.append(movieTitle)
    config.listings.update_one({"id":ID}, {"$set":{"movies":movies}})
    file = open("static/movieList.txt", "r")
    allTitles = file.readlines()
    file.close()
    return render_template('watchlist.html', listName=listName, movies=movies, ID=ID, allTitles=allTitles)
    
    
@app.route('/deleteFromList', methods = ['POST']) 
def deleteFromList():
    ID = request.form['id'] 
    multiselect = request.form.getlist('list')
    data = config.listings.find_one({"id":ID})
    listName = data["name"]
    movies = data["movies"]
    for movieTitle in multiselect:
        movies.remove(movieTitle)
    config.listings.update_one({"id":ID}, {"$set":{"movies":movies}})
    file = open("static/movieList.txt", "r")
    allTitles = file.readlines()
    file.close()
    return render_template('watchlist.html', listName=listName, movies=movies, ID=ID, allTitles=allTitles)
    
    
    
@app.errorhandler(404)
def page_not_found(e):
    error = "Sorry. Page not found. Try creating a new list."
    return render_template('index.html', error=error), 404 
    

if __name__ == "__main__":
    app.run()
   