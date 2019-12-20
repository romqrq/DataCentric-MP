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

@app.route('/add_task')
def add_task():
    return render_template('addtask.html',
    categories=mongo.db.categories.find())

#We specified POST here, default is GET
@app.route('/insert_task', methods=['POST'])
    #Here, because we're submitting a form and we're submitting using POST, we must refer to the HTTP method
    #that will be used to deliver the form data
def insert_task():
    #get the tasks collection
    tasks = mongo.db.tasks
    #Whenever submitting information to a URI or to some web location, it is submitted in the form of a 
    #REQUEST OBJECT. inside that we say show me the FORM and we convert the form, in this case, TO A DICTIONARY
    #so it can be easily understood by Mongo.
    #do an INSERT_ONE and insert
    tasks.insert_one(request.form.to_dict())
    #Any of the FORM FIELDS that have data inside them, or are active, will be submitted as part of the form submission
    #and ultimately, we'll go on to CREATE a new document in our TASK COLLECTION

    #Once this is done, we redirect to get_tasks, so we can view that new task in our collection
    return redirect(url_for('get_tasks'))

    #IN REAL LIFE, DO SOME VALIDATION both on the HTML and here for REQUIRED FIELDS

@app.route('/edit_task/<task_id>')
def edit_task(task_id):
    the_task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})
    all_categories = mongo.db.categories.find()
    return render_template('edittask.html', task=the_task, categories=all_categories)

@app.route('/update_task/<task_id>', methods=["POST"])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
    {
        'task_name':request.form.get('task_name'),
        'category_name':request.form.get('category_name'),
        'task_description':request.form.get('task_description'),
        'due_date':request.form.get('due_date'),
        'is_urgent':request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))

@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories = mongo.db.categories.find())

@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update({'_id': ObjectId(category_id)}, {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))

@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))

@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form.get('category_name')}
    categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))

@app.route('/new_category')
def new_category():
    return render_template('addcategory.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)