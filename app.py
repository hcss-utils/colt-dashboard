from flask import Flask, send_from_directory, redirect, url_for, render_template_string
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

# Add routes for image files
@app.route('/trips_per_year.png')
def trips_per_year():
    return send_from_directory('static', 'trips_per_year.png')

@app.route('/top_destinations.png')
def top_destinations():
    return send_from_directory('static', 'top_destinations.png')

@app.route('/region_distribution.png')
def region_distribution():
    return send_from_directory('static', 'region_distribution.png')

@app.route('/trip_duration.png')
def trip_duration():
    return send_from_directory('static', 'trip_duration.png')

@app.route('/top_leaders.png')
def top_leaders():
    return send_from_directory('static', 'top_leaders.png')

@app.route('/region_flow_heatmap.png')
def region_flow_heatmap():
    return send_from_directory('static', 'region_flow_heatmap.png')

@app.route('/health')
def health():
    """Health check endpoint for Heroku"""
    return "OK"

if __name__ == '__main__':
    # Get port from environment variable for Heroku compatibility
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)