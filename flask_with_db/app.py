from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import socket
import os

app = Flask(__name__)

# MongoDB connection
mongo_uri = os.environ.get('MONGO_URI')
client = MongoClient(mongo_uri)  # Connect to MongoDB container
db = client["projectdb"]  # Database name
collection = db["requests"]  # Collection name

@app.route('/')
def home():
    # Get server details
    hostname = socket.gethostname()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Record request details in MongoDB
    client_ip = request.remote_addr
    collection.insert_one({"ip": client_ip, "date": current_date})
    
    # Get the last 10 records from MongoDB
    records = list(collection.find().sort("_id", -1).limit(10))
    records_display = [{"ip": record["ip"], "date": record["date"]} for record in records]

    return jsonify({
        "developer_name": "Your Name",
        "project_name": "Your Project Name",
        "version": "V2",
        "server_hostname": hostname,
        "current_date": current_date,
        "last_10_records": records_display
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
