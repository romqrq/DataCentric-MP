import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

#MongoDB Stores its data in a JSON-like format called BSON so we are importing this from the
#BSON library.

#After importing the Flask functionality, we need to create an instance of Flask or Flask app
app = Flask(__name__)
#Adding the MONGO DATABASE NAME and the URL linking to that database
app.config["MONGO_DBNAME"] = 'task_manager'
# app.config["MONGO_URI"] = 'mongodb+srv://root:R0mul0ng0u5@myfirstcluster-reumj.mongodb.net/task_manager?retryWrites=true&w=majority'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')
#Getting MONGO_URI from the environment variables
# MONGO_URI = os.getenv("MONGO_URI")

#Creating an instance of PyMongo. We'll add the app into a CONSTRUCTOR METHOD
mongo = PyMongo(app)
#Creating a test function with a route in it that will display some text as proof of concept
#The / refers to the default route
@app.route('/')

#Setting up to make our connection to the database
# Because od the decorator with '/', the default function that will be called will be GET_TASKS
@app.route('/get_tasks')

def get_tasks():
    #Rendering a template and supplying a TASKS COLLECTION(mongo.db.TASKS.find()) which will be returned from making a call 
    #directly to MONGO. The FIND() method will return everything from our tasks collection
    return render_template('tasks.html', tasks=mongo.db.tasks.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)