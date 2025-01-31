from flask import Flask, render_template_string
from datetime import datetime
import socket

app = Flask(__name__)

@app.route('/')
def home():
  
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

    </body>
    </html>
    """
     # Get server details
    hostname = socket.gethostname()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')



    return render_template_string (
        html_content,
        developer_name="Victor",
        project_name="Kubernetes",
        version="V1.1",
        server_hostname=hostname,
        current_date=current_date,
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
