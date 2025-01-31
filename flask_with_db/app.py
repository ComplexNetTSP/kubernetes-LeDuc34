from flask import Flask, request, render_template_string
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

    # HTML content
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ project_name }}</title>
    </head>
    <body>
        <h1>Welcome to {{ project_name }}</h1>
        <p><strong>Developer:</strong> {{ developer_name }}</p>
        <p><strong>Version:</strong> {{ version }}</p>
        <p><strong>Hostname:</strong> {{ server_hostname }}</p>
        <p><strong>Current Date:</strong> {{ current_date }}</p>
        
        <h2>Last 10 Records</h2>
        <ul>
            {% for record in last_10_records %}
                <li>IP: {{ record.ip }}, Date: {{ record.date }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """

    # Render the HTML with the provided data
    return render_template_string(
        html_content,
        developer_name="Victor",
        project_name="Kubernetes",
        version="V1.1",
        server_hostname=hostname,
        current_date=current_date,
        last_10_records=records_display
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
