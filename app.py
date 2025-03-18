from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main dashboard HTML file"""
    return send_from_directory('static', 'colt_complete_dashboard.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files from the static directory"""
    return send_from_directory('static', path)

@app.route('/<path:filename>')
def serve_files_in_root(filename):
    """Serve files from static directory when requested at root URL path"""
    return send_from_directory('static', filename)

@app.route('/health')
def health():
    """Health check endpoint for Heroku"""
    return "OK"

if __name__ == '__main__':
    # Get port from environment variable for Heroku compatibility
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)