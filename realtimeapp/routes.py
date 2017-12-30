from flask import render_template
from . import app

# Make sure these routes are not already in use on "restful" __init__.py 
@app.route('/')
def index():
    return render_template('index.html')