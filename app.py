import os
from flask import Flask

#After importing the Flask functionality, we need to create an instance of Flask or Flask app
app = Flask(__name__)

#Creating a test function with a route in it that will display some text as proof of concept
#The / refers to the default route
@app.route('/')

def hello():
    return 'Hello Worls...again'

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)