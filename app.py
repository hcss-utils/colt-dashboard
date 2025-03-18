from flask import Flask, send_from_directory, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    """Serve the main dashboard HTML file"""
    return send_from_directory('static', 'colt_complete_dashboard.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

# Add specific routes for each visualization
@app.route('/comprehensive_trips_viz.html')
def comprehensive_viz():
    return send_from_directory('static', 'comprehensive_trips_viz.html')

@app.route('/country_pair_viz.html')
def country_pair_viz():
    return send_from_directory('static', 'country_pair_viz.html')

@app.route('/leader_timeline_viz.html')
def leader_timeline_viz():
    return send_from_directory('static', 'leader_timeline_viz.html')

@app.route('/diversity_viz.html')
def diversity_viz():
    return send_from_directory('static', 'diversity_viz.html')

@app.route('/health')
def health():
    """Health check endpoint for Heroku"""
    return "OK"

if __name__ == '__main__':
    # Get port from environment variable for Heroku compatibility
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)