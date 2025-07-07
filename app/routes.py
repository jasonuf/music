from flask import render_template
from app import app
from app.shared_state import shared_data, data_lock

@app.route('/')
@app.route('/index')
def index():
    with data_lock:
        result = shared_data.get("recently_played", [])
        
    return render_template('index.html', data=result)

@app.route('/callback')
def callback():
    return "Callback"