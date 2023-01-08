from flask import Flask
import os


app = Flask(__name__)



@app.route('/')
def home():
    return 'You are at home page.'


 
# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)