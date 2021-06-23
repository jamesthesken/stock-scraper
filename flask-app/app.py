from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import time
import requests
from arctic import Arctic

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return jsonify({'time': time.time()})

@app.route('/v1/tickers')
def get_ticks():
    # Connect to Local MONGODB
    store = Arctic('localhost')

    # Create the library - defaults to VersionStore
    store.initialize_library('REDDIT')

    # Access the library
    library = store['REDDIT']

    # Reading the data
    item = library.read('WSB')
    
    gme = item.data.to_json(orient="table")
    metadata = item.metadata

    print(metadata)
    return(gme)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)