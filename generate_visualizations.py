import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tqdm.auto import tqdm
import shutil

# Create static folder if it doesn't exist
if not os.path.exists('static'):
    os.makedirs('static')

# Load the CSV file
print("Loading data...")
df = pd.read_csv("Diplometrics_COLT_Travel_Dataset_Primary-HOGS-1990-2024_20250317.csv", 
                 encoding='latin1', low_memory=False)

# Fix the TripDuration column
print("Processing TripDuration data...")
df['TripDuration'] = pd.to_numeric(df['TripDuration'].replace('TBD', np.nan), errors='coerce')
print(f"Data loaded with {len(df)} rows and {len(df.columns)} columns")

# Set the tab20 color palette for all visualizations
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab20.colors)

# Create a list to track visualizations
visualizations = []

# 1. Trips per year over time with tab20 colors
def plot_trips_per_year():
    trips_per_year = df['TripYear'].value_counts().sort_index()
    plt.figure(figsize=(14, 8))
    ax = trips_per_year.plot(kind='line', marker='o', linewidth=3, 
                        color=plt.cm.tab20.colors[0], markersize=8)
    # Add points with different color
    plt.scatter(trips_per_year.index, trips_per_year.values, 
                color=plt.cm.tab20.colors[1], s=100, zorder=5)
    plt.title('Diplomatic Travel Trends: Number of Head of Government Trips per Year (1990-2024)',
              fontsize=18, fontweight='bold')
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Number of Trips', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Annotate max and min
    max_year = trips_per_year.idxmax()
    min_year = trips_per_year.idxmin()
    plt.annotate(f'Max: {trips_per_year.max()}', 
                xy=(max_year, trips_per_year.max()), 
                xytext=(max_year+0.5, trips_per_year.max()+100),
                arrowprops=dict(facecolor=plt.cm.tab20.colors[2], shrink=0.05),
                fontsize=12)
    plt.annotate(f'Min: {trips_per_year.min()}', 
                xy=(min_year, trips_per_year.min()), 
                xytext=(min_year-1, trips_per_year.min()-200),
                arrowprops=dict(facecolor=plt.cm.tab20.colors[3], shrink=0.05),
                fontsize=12)
    
    plt.tight_layout()
    plt.savefig('trips_per_year.png', dpi=300)
    plt.close()  # Close the figure
visualizations.append(("Trips per year", plot_trips_per_year))

# 2. Top 10 destination countries with custom tab20 colors
def plot_top_destinations():
    top_destinations = df['CountryVisited'].value_counts().head(10)
    plt.figure(figsize=(14, 8))
    bars = plt.barh(top_destinations.index[::-1], top_destinations.values[::-1], 
                    color=plt.cm.tab20.colors[:10])
    
    # Add value labels
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 50, bar.get_y() + bar.get_height()/2, 
                f'{top_destinations.values[::-1][i]:,}', 
                va='center', fontsize=12, fontweight='bold')
    
    plt.title('Top 10 Destinations for Head of Government Diplomatic Visits', 
              fontsize=18, fontweight='bold')
    plt.xlabel('Number of Visits', fontsize=14)
    plt.ylabel('Country', fontsize=14)
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('top_destinations.png', dpi=300)
    plt.close()  # Close the figure
visualizations.append(("Top destinations", plot_top_destinations))

# 3. Regional travel analysis with tab20 colors
def plot_region_visits():
    region_visits = df['RegionVisited'].value_counts()
    plt.figure(figsize=(12, 10))
    
    # Create pie chart with tab20 colors
    patches, texts, autotexts = plt.pie(region_visits.values, 
                                       labels=region_visits.index, 
                                       autopct='%1.1f%%', 
                                       shadow=True, 
                                       startangle=90,
                                       colors=plt.cm.tab20.colors[:len(region_visits)])
    
    # Enhance text appearance
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
        
    plt.title('Distribution of Head of Government Visits by Region', 
              fontsize=18, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('region_distribution.png', dpi=300)
    plt.close()  # Close the figure
visualizations.append(("Region visits", plot_region_visits))

# 4. Trip duration distribution with tab20 colors
def plot_trip_duration():
    plt.figure(figsize=(14, 8))
    
    # Create histogram - Fixed to avoid kde_kws parameter issue
    ax = sns.histplot(df['TripDuration'].dropna(), bins=30, kde=False, 
                     color=plt.cm.tab20.colors[4])
    
    # Add separate KDE line with different color
    sns.kdeplot(df['TripDuration'].dropna(), color=plt.cm.tab20.colors[5], linewidth=3)
    
    # Add statistics to the plot
    mean_dur = df['TripDuration'].mean()
    median_dur = df['TripDuration'].median()
    
    plt.axvline(mean_dur, color=plt.cm.tab20.colors[6], linestyle='--', linewidth=2, 
                label=f'Mean: {mean_dur:.1f} days')
    plt.axvline(median_dur, color=plt.cm.tab20.colors[7], linestyle='-.', linewidth=2, 
                label=f'Median: {median_dur:.1f} days')
    
    plt.title('Distribution of Diplomatic Trip Durations', 
              fontsize=18, fontweight='bold')
    plt.xlabel('Trip Duration (Days)', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('trip_duration.png', dpi=300)
    plt.close()  # Close the figure
visualizations.append(("Trip duration", plot_trip_duration))

# 5. Heatmap of trips between regions with custom colormap
def plot_region_heatmap():
    if 'LeaderRegion' in df.columns and 'RegionVisited' in df.columns:
        region_matrix = pd.crosstab(df['LeaderRegion'], df['RegionVisited'])
        
        # Create a custom colormap using tab20 colors
        from matplotlib.colors import LinearSegmentedColormap
        tab20_subset = plt.cm.tab20(np.linspace(0, 1, 20))
        custom_cmap = LinearSegmentedColormap.from_list('tab20_custom', 
                                                      [tab20_subset[0], tab20_subset[4], 
                                                       tab20_subset[8], tab20_subset[12]])
        
        plt.figure(figsize=(16, 12))
        sns.heatmap(region_matrix, annot=True, cmap=custom_cmap, fmt='d', 
                   linewidths=1, linecolor='white')
        
        plt.title('Heatmap of Diplomatic Travel Flows Between Regions', 
                  fontsize=18, fontweight='bold')
        plt.xlabel('Region Visited', fontsize=14)
        plt.ylabel('Leader\'s Region', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()
        plt.savefig('region_flow_heatmap.png', dpi=300)
        plt.close()  # Close the figure
visualizations.append(("Region heatmap", plot_region_heatmap))

# 6. Top leaders by number of trips with tab20 colors
def plot_top_leaders():
    # Combine leader name and country
    df['LeaderFullInfo'] = df['LeaderFullName'] + ' (' + df['LeaderCountryOrIGO'] + ')'
    
    # Get top 15 leaders by number of trips
    top_leaders = df['LeaderFullInfo'].value_counts().head(15)
    
    plt.figure(figsize=(14, 10))
    bars = plt.barh(top_leaders.index[::-1], top_leaders.values[::-1], 
                   color=plt.cm.tab20c.colors[:15])
    
    # Add value labels
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 10, bar.get_y() + bar.get_height()/2, 
                f'{top_leaders.values[::-1][i]:,}', 
                va='center', fontsize=11, fontweight='bold')
    
    plt.title('Top 15 Leaders by Number of Diplomatic Trips', 
              fontsize=18, fontweight='bold')
    plt.xlabel('Number of Trips', fontsize=14)
    plt.ylabel('Leader', fontsize=14)
    plt.grid(True, alpha=0.3, axis='x')
    plt.tight_layout()
    plt.savefig('top_leaders.png', dpi=300)
    plt.close()  # Close the figure
visualizations.append(("Top leaders", plot_top_leaders))

# Create a comprehensive interactive visualization
def create_comprehensive_interactive_viz():
    print("Creating comprehensive interactive visualization...")
    
    # Get top 15 countries by number of visits
    top_visited_countries = df['CountryVisited'].value_counts().head(15).index.tolist()
    
    # Get top 15 countries by number of diplomatic trips
    top_leader_countries = df['LeaderCountryOrIGO'].value_counts().head(15).index.tolist()
    
    # Get top 15 countries by number of countries visited
    country_diversity = df.groupby('LeaderCountryOrIGO')['CountryVisited'].nunique().sort_values(ascending=False).head(15)
    diverse_countries = country_diversity.index.tolist()
    
    # Create yearly counts for all countries
    data_frames = []
    
    # Process visited countries
    for country in tqdm(top_visited_countries, desc="Processing visited countries"):
        country_data = df[df['CountryVisited'] == country].groupby('TripYear').size().reset_index(name='Trips')
        country_data['Country'] = country
        country_data['Type'] = 'Visited'
        data_frames.append(country_data)
    
    # Process leader countries
    for country in tqdm(top_leader_countries, desc="Processing leader countries"):
        country_data = df[df['LeaderCountryOrIGO'] == country].groupby('TripYear').size().reset_index(name='Trips')
        country_data['Country'] = country
        country_data['Type'] = 'Visiting'
        data_frames.append(country_data)
    
    # Process diverse countries
    for country in tqdm(diverse_countries, desc="Processing diverse countries"):
        country_data = df[df['LeaderCountryOrIGO'] == country].groupby('TripYear').size().reset_index(name='Trips')
        country_data['Country'] = country
        country_data['Type'] = 'Diverse'
        data_frames.append(country_data)
    
    combined_df = pd.concat(data_frames)
    
    # Create the figure with tabs for different visualizations
    fig = go.Figure()
    
    # Create three separate visualizations
    
    # 1. Top 15 Visited Countries - All visible by default
    for country in top_visited_countries:
        country_data = combined_df[(combined_df['Country'] == country) & (combined_df['Type'] == 'Visited')]
        fig.add_trace(
            go.Scatter(
                x=country_data['TripYear'],
                y=country_data['Trips'],
                mode='lines+markers',
                name=f"{country} (Visited)",
                visible=True,  # Show all by default
                line=dict(width=3)
            )
        )
    
    # 2. Top 15 Countries by Number of Diplomatic Trips
    for country in top_leader_countries:
        country_data = combined_df[(combined_df['Country'] == country) & (combined_df['Type'] == 'Visiting')]
        fig.add_trace(
            go.Scatter(
                x=country_data['TripYear'],
                y=country_data['Trips'],
                mode='lines+markers',
                name=f"{country} (Visiting)",
                visible=False,  # Hide initially
                line=dict(width=3)
            )
        )
    
    # 3. Top 15 Countries by Diversity of Countries Visited
    for country in diverse_countries:
        country_data = combined_df[(combined_df['Country'] == country) & (combined_df['Type'] == 'Diverse')]
        fig.add_trace(
            go.Scatter(
                x=country_data['TripYear'],
                y=country_data['Trips'],
                mode='lines+markers',
                name=f"{country} (Diverse)",
                visible=False,  # Hide initially
                line=dict(width=3)
            )
        )
    
    # Create buttons for category selection
    buttons = [
        dict(
            label="<b>Top 15 Visited Countries</b>",
            method="update",
            args=[
                {"visible": [i < len(top_visited_countries) for i in range(len(fig.data))]},
                {"title": "Top 15 Most Visited Countries (1990-2024)"}
            ]
        ),
        dict(
            label="<b>Top 15 Visiting Countries</b>",
            method="update",
            args=[
                {"visible": [len(top_visited_countries) <= i < len(top_visited_countries) + len(top_leader_countries) for i in range(len(fig.data))]},
                {"title": "Top 15 Countries by Number of Diplomatic Trips (1990-2024)"}
            ]
        ),
        dict(
            label="<b>Top 15 Most Diverse Countries</b>",
            method="update",
            args=[
                {"visible": [i >= len(top_visited_countries) + len(top_leader_countries) for i in range(len(fig.data))]},
                {"title": "Top 15 Countries by Diversity of Destinations (1990-2024)"}
            ]
        )
    ]
    
    # Update layout with menus
    fig.update_layout(
        title="Top 15 Most Visited Countries (1990-2024)",
        title_font_size=24,
        xaxis_title="Year",
        yaxis_title="Number of Trips",
        template="plotly_white",
        height=700,
        width=1100,
        legend=dict(
            font=dict(size=12),
            itemsizing='constant'
        ),
        updatemenus=[
            # Category selector
            dict(
                buttons=buttons,
                direction="down",
                showactive=True,
                x=0.25,
                xanchor="center",
                y=1.15,
                yanchor="top",
                bgcolor="lightblue",
                bordercolor="royalblue",
                font=dict(size=14),
                pad=dict(l=10, r=10, t=10, b=10)
            )
        ],
        annotations=[
            dict(
                text="<b>Select Category:</b>",
                showarrow=False,
                x=0.25,
                y=1.22,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                font=dict(size=16, color="royalblue")
            )
        ]
    )
    
    # Save the figure
    fig.write_html("comprehensive_trips_viz.html")
    return fig

# Create an improved country-pair visualization with dyadic selection
def create_country_pair_viz():
    print("Creating improved country pair visualization for dyadic analysis...")
    
    # Get unique visiting and visited countries
    all_visiting = sorted(df['LeaderCountryOrIGO'].unique())
    all_visited = sorted(df['CountryVisited'].unique())
    
    # Get top 15 for initial display
    top_visiting = df['LeaderCountryOrIGO'].value_counts().head(15).index.tolist()
    top_visited = df['CountryVisited'].value_counts().head(15).index.tolist()
    
    # Create figure with subplot for dropdown controls
    fig = make_subplots(rows=1, cols=1)
    
    # Dictionary to store dyad data
    dyad_data = {}
    
    # Process top dyads for initial display
    print("Processing initial dyads...")
    for visiting in tqdm(top_visiting[:5]):
        for visited in top_visited[:5]:
            if visiting == visited:
                continue
                
            pair_df = df[(df['LeaderCountryOrIGO'] == visiting) & (df['CountryVisited'] == visited)]
            if len(pair_df) > 0:
                yearly = pair_df.groupby('TripYear').size().reset_index(name='Visits')
                pair_name = f"{visiting} → {visited}"
                
                # Store data for this dyad
                dyad_data[(visiting, visited)] = yearly
                
                # Add trace
                fig.add_trace(
                    go.Scatter(
                        x=yearly['TripYear'],
                        y=yearly['Visits'],
                        mode='lines+markers',
                        name=pair_name,
                        line=dict(width=3)
                    )
                )
    
    # Create HTML with JavaScript for dynamic dyad selection
    # This will allow for any visiting/visited country selection
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Country Pair Analysis</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .description {
                margin-bottom: 20px;
            }
            .control-panel {
                display: flex;
                justify-content: space-around;
                align-items: center;
                padding: 15px;
                background-color: #eef6ff;
                border-radius: 5px;
                margin-bottom: 20px;
            }
            .selector-group {
                display: flex;
                flex-direction: column;
                margin: 0 10px;
            }
            .selector-group label {
                font-weight: bold;
                margin-bottom: 5px;
                color: #0066cc;
            }
            select {
                padding: 8px;
                border-radius: 4px;
                border: 1px solid #ccc;
                min-width: 200px;
            }
            button {
                padding: 8px 15px;
                background-color: #0066cc;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-weight: bold;
            }
            button:hover {
                background-color: #0055aa;
            }
            #plotContainer {
                height: 600px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Diplomatic Visits Between Countries</h1>
            <div class="description">
                This visualization allows you to analyze diplomatic visits between specific country pairs over time. 
                Select both a visiting country and a visited country to see their specific relationship, or use the
                pre-loaded options to explore key diplomatic relationships.
            </div>
            
            <div class="control-panel">
                <div class="selector-group">
                    <label for="visitingCountry">Select Visiting Country:</label>
                    <select id="visitingCountry">
                        <option value="">-- Select a country --</option>
                        {{ VISITING_OPTIONS }}
                    </select>
                </div>
                
                <div class="selector-group">
                    <label for="visitedCountry">Select Visited Country:</label>
                    <select id="visitedCountry">
                        <option value="">-- Select a country --</option>
                        {{ VISITED_OPTIONS }}
                    </select>
                </div>
                
                <button onclick="updateDyadView()">View Relationship</button>
            </div>
            
            <div class="selector-group">
                <label for="predefinedPair">Or select a pre-defined country pair:</label>
                <select id="predefinedPair" onchange="selectPredefinedPair()">
                    <option value="">-- Select a pre-defined pair --</option>
                    {{ PAIR_OPTIONS }}
                </select>
            </div>
            
            <div id="plotContainer"></div>
        </div>
        
        <script>
            // Store the data for pre-processed dyads
            const dyadData = {
                {{ DYAD_DATA }}
            };
            
            // Initial plot data
            const initialData = {{ INITIAL_DATA }};
            
            // Create initial plot
            const layout = {
                title: 'Diplomatic Visits Between Countries Over Time',
                xaxis: { title: 'Year' },
                yaxis: { title: 'Number of Visits' },
                hovermode: 'closest',
                template: 'plotly_white'
            };
            
            Plotly.newPlot('plotContainer', initialData, layout);
            
            // Function to update the plot based on country selections
            function updateDyadView() {
                const visitingCountry = document.getElementById('visitingCountry').value;
                const visitedCountry = document.getElementById('visitedCountry').value;
                
                if (!visitingCountry || !visitedCountry) {
                    alert('Please select both a visiting country and a visited country');
                    return;
                }
                
                if (visitingCountry === visitedCountry) {
                    alert('Please select different countries for visiting and visited');
                    return;
                }
                
                const pairKey = `${visitingCountry}_${visitedCountry}`;
                
                // Check if we have pre-computed data
                if (dyadData[pairKey]) {
                    // Update the plot with pre-computed data, ensuring x and y are arrays
                    const trace = {
                        x: Array.isArray(dyadData[pairKey].x) ? dyadData[pairKey].x : [dyadData[pairKey].x],
                        y: Array.isArray(dyadData[pairKey].y) ? dyadData[pairKey].y : [dyadData[pairKey].y],
                        mode: 'lines+markers',
                        name: `${visitingCountry} → ${visitedCountry}`,
                        line: { width: 3 }
                    };
                    
                    Plotly.react('plotContainer', [trace], {
                        ...layout,
                        title: `Diplomatic Visits: ${visitingCountry} → ${visitedCountry} (1990-2024)`
                    });
                } else {
                    // Display a placeholder message
                    Plotly.react('plotContainer', [], {
                        ...layout,
                        title: `No recorded diplomatic visits from ${visitingCountry} to ${visitedCountry}`,
                        annotations: [{
                            text: 'No data available for this specific country pair',
                            showarrow: false,
                            font: { size: 16 },
                            x: 0.5,
                            y: 0.5,
                            xref: 'paper',
                            yref: 'paper'
                        }]
                    });
                }
            }
            
            // Function to handle pre-defined pair selection
            function selectPredefinedPair() {
                const pairValue = document.getElementById('predefinedPair').value;
                if (!pairValue) return;
                
                const [visiting, visited] = pairValue.split('_');
                
                // Update the dropdowns
                document.getElementById('visitingCountry').value = visiting;
                document.getElementById('visitedCountry').value = visited;
                
                // Update the view
                updateDyadView();
            }
        </script>
    </body>
    </html>
    """
    
    # Generate visiting country options
    visiting_options = ""
    for country in all_visiting:
        visiting_options += f'<option value="{country}">{country}</option>\n'
    
    # Generate visited country options
    visited_options = ""
    for country in all_visited:
        visited_options += f'<option value="{country}">{country}</option>\n'
    
    # Generate pair options for the top relationships
    pair_options = ""
    top_pairs = []
    
    for visiting in top_visiting:
        for visited in top_visited:
            if visiting != visited and (visiting, visited) in dyad_data:
                pair_options += f'<option value="{visiting}_{visited}">{visiting} → {visited}</option>\n'
                top_pairs.append((visiting, visited))
    
    # Generate JavaScript data object for pre-computed dyads
    dyad_js_data = ""
    for (visiting, visited), data in dyad_data.items():
        key = f"{visiting}_{visited}"        
        x_values = json.dumps(data['TripYear'].tolist())
        y_values = json.dumps(data['Visits'].tolist())
        dyad_js_data += f'"{key}": {{ "x": {x_values}, "y": {y_values} }},\n'
    
    # Create initial data JSON for Plotly
    initial_data = "["
    for i, (visiting, visited) in enumerate(list(dyad_data.keys())[:5]):  # First 5 pairs
        data = dyad_data[(visiting, visited)]
        x_values = data['TripYear'].tolist()
        y_values = data['Visits'].tolist()
        
        initial_data += f"""
        {{
            "x": {x_values},
            "y": {y_values},
            "mode": "lines+markers",
            "name": "{visiting} → {visited}",
            "line": {{ "width": 3 }}
        }}{"," if i < 4 else ""}
        """
    initial_data += "]"
    
    # Replace placeholders
    html_content = html_template
    html_content = html_content.replace("{{ VISITING_OPTIONS }}", visiting_options)
    html_content = html_content.replace("{{ VISITED_OPTIONS }}", visited_options)
    html_content = html_content.replace("{{ PAIR_OPTIONS }}", pair_options)
    html_content = html_content.replace("{{ DYAD_DATA }}", dyad_js_data)
    html_content = html_content.replace("{{ INITIAL_DATA }}", initial_data)
    
    # Write HTML to file
    with open("country_pair_viz.html", "w") as f:
        f.write(html_content)
    
    print("Dynamic country pair visualization created")
    return fig

# Create leader timeline visualization
def create_leader_timeline():
    print("Creating leader timeline visualization...")
    
    # Get top 15 leaders by number of trips
    df['LeaderFullInfo'] = df['LeaderFullName'] + ' (' + df['LeaderCountryOrIGO'] + ')'
    top_leaders = df['LeaderFullInfo'].value_counts().head(15)
    
    leader_data = []
    
    # Process data for each top leader
    for leader in tqdm(top_leaders.index, desc="Processing leaders"):
        leader_df = df[df['LeaderFullInfo'] == leader]
        yearly_data = leader_df.groupby('TripYear').size().reset_index(name='Trips')
        yearly_data['Leader'] = leader
        leader_data.append(yearly_data)
    
    combined_leaders = pd.concat(leader_data)
    
    # Create interactive figure
    fig = px.line(
        combined_leaders,
        x='TripYear',
        y='Trips',
        color='Leader',
        title='Diplomatic Activity of Top 15 Leaders Over Time',
        labels={'TripYear': 'Year', 'Trips': 'Number of Trips'},
        line_shape='linear',
        markers=True
    )
    
    # Update layout
    fig.update_layout(
        height=700,
        width=1100,
        xaxis_title="Year",
        yaxis_title="Number of Trips",
        legend_title="Leaders"
    )
    
    # Save the figure
    fig.write_html("leader_timeline_viz.html")
    return fig

# Create diplomatic diversity visualization
def create_diversity_viz():
    print("Creating diplomatic diversity visualization...")
    
    # Calculate diversity metrics by year and country
    yearly_diversity = []
    
    # Process data by year
    for year in tqdm(sorted(df['TripYear'].unique()), desc="Processing years"):
        year_df = df[df['TripYear'] == year]
        
        # Calculate for each country
        for country in year_df['LeaderCountryOrIGO'].unique():
            country_year_df = year_df[year_df['LeaderCountryOrIGO'] == country]
            
            # Skip if no data
            if len(country_year_df) == 0:
                continue
                
            # Calculate metrics
            num_trips = len(country_year_df)
            num_countries = country_year_df['CountryVisited'].nunique()
            avg_duration = country_year_df['TripDuration'].mean()
            
            yearly_diversity.append({
                'Year': year,
                'Country': country,
                'TotalTrips': num_trips,
                'UniqueDestinations': num_countries,
                'DestinationsPerTrip': num_countries / num_trips if num_trips > 0 else 0,
                'AvgDuration': avg_duration
            })
    
    diversity_df = pd.DataFrame(yearly_diversity)

    # Get top 15 countries by total unique destinations
    country_totals = diversity_df.groupby('Country')['UniqueDestinations'].sum().sort_values(ascending=False).head(15)
    top_diverse_countries = country_totals.index.tolist()
    
    # Filter data to top countries
    filtered_diversity = diversity_df[diversity_df['Country'].isin(top_diverse_countries)]
    
    # Create bubble chart with multiple metrics
    fig = px.scatter(
        filtered_diversity,
        x='Year',
        y='Country',
        size='TotalTrips',
        color='UniqueDestinations',
        hover_data=['AvgDuration', 'DestinationsPerTrip'],
        title='Diplomatic Diversity: Travel Patterns of Top 15 Countries (1990-2024)',
        height=800,
        width=1100,
        color_continuous_scale='Viridis',
        size_max=40
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Country",
        coloraxis_colorbar_title="Unique Destinations",
        legend_title="Metrics",
        font=dict(size=14),
        title_font_size=20
    )
    
    # Save the figure
    fig.write_html("diversity_viz.html")
    return fig

# Create a comprehensive dashboard HTML
def create_complete_dashboard():
    print("Creating comprehensive dashboard HTML...")
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>COLT Dataset Analysis Dashboard</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1, h2, h3 {
                color: #333;
            }
            h1 {
                text-align: center;
                padding: 20px 0;
                border-bottom: 2px solid #ddd;
            }
            .section {
                background: white;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .viz-container {
                margin-top: 30px;
            }
            .img-container {
                margin: 20px 0;
                text-align: center;
            }
            .img-container img {
                max-width: 100%;
                height: auto;
                border-radius: 4px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            iframe {
                width: 100%;
                height: 700px;
                border: none;
                margin: 20px 0;
                border-radius: 4px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .footer {
                text-align: center;
                padding: 20px;
                color: #666;
                font-size: 0.9em;
                margin-top: 50px;
                border-top: 1px solid #ddd;
            }
            .tabs {
                display: flex;
                margin: 20px 0;
                border-bottom: 1px solid #ddd;
                flex-wrap: wrap;
            }
            .tab {
                padding: 10px 20px;
                cursor: pointer;
                border: 1px solid #ddd;
                border-bottom: none;
                border-radius: 5px 5px 0 0;
                background-color: #f1f1f1;
                margin-right: 5px;
                margin-bottom: 5px;
            }
            .tab.active {
                background-color: white;
                border-bottom: 1px solid white;
                margin-bottom: -1px;
            }
            .tab-content {
                display: none;
                padding: 20px;
                border: 1px solid #ddd;
                border-top: none;
                border-radius: 0 0 5px 5px;
            }
            .tab-content.active {
                display: block;
            }
            .grid-container {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                margin: 20px 0;
            }
            @media (max-width: 800px) {
                .grid-container {
                    grid-template-columns: 1fr;
                }
            }
            .grid-item {
                background: white;
                padding: 15px;
                border-radius: 5px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        </style>
        <script>
            function openTab(evt, tabName) {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tab-content");
                for (i = 0; i < tabcontent.length; i++) {
                    tabcontent[i].className = tabcontent[i].className.replace(" active", "");
                }
                tablinks = document.getElementsByClassName("tab");
                for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }
                document.getElementById(tabName).className += " active";
                evt.currentTarget.className += " active";
            }
            
            window.onload = function() {
                // Open the first tab by default
                document.getElementsByClassName("tab")[0].click();
            };
        </script>
    </head>
    <body>
        <h1>COLT Dataset - Comprehensive Diplomatic Travel Analysis Dashboard</h1>
        
        <div class="section">
            <h2>About the Dataset</h2>
            <p>This dashboard provides a comprehensive analysis of the Country and Organization Leader Travel (COLT) dataset from the Frederick S. Pardee Institute for International Futures at the University of Denver. The dataset tracks diplomatic travel of heads of government and state from 1990 to 2024, offering insights into global diplomatic relations, patterns, and trends.</p>
        </div>
        
        <div class="section">
            <h2>Dashboard Contents</h2>
            
            <div class="tabs">
                <button class="tab" onclick="openTab(event, 'tab-static')">Static Visualizations</button>
                <button class="tab" onclick="openTab(event, 'tab-comprehensive')">Top Countries & Leaders</button>
                <button class="tab" onclick="openTab(event, 'tab-country-pairs')">Country Pair Analysis</button>
                <button class="tab" onclick="openTab(event, 'tab-leader-timeline')">Leader Timeline</button>
                <button class="tab" onclick="openTab(event, 'tab-diversity')">Diplomatic Diversity</button>
            </div>
            
            <div id="tab-static" class="tab-content">
                <h3>Static Visualizations</h3>
                <p>These visualizations provide a comprehensive overview of diplomatic travel patterns from the COLT dataset.</p>
                
                <div class="grid-container">
                    <div class="grid-item">
                        <h4>Diplomatic Trips Over Time</h4>
                        <div class="img-container">
                            <img src="trips_per_year.png" alt="Trips per year">
                        </div>
                        <p>This visualization shows the number of diplomatic trips taken by heads of government each year from 1990 to 2024.</p>
                    </div>
                    
                    <div class="grid-item">
                        <h4>Top Destinations</h4>
                        <div class="img-container">
                            <img src="top_destinations.png" alt="Top destinations">
                        </div>
                        <p>This chart displays the top 10 most visited countries by heads of government.</p>
                    </div>
                    
                    <div class="grid-item">
                        <h4>Regional Distribution</h4>
                        <div class="img-container">
                            <img src="region_distribution.png" alt="Region distribution">
                        </div>
                        <p>This pie chart shows the distribution of diplomatic visits across different regions of the world.</p>
                    </div>
                    
                    <div class="grid-item">
                        <h4>Trip Duration</h4>
                        <div class="img-container">
                            <img src="trip_duration.png" alt="Trip duration">
                        </div>
                        <p>This histogram displays the distribution of diplomatic trip durations, with the mean and median highlighted.</p>
                    </div>
                    
                    <div class="grid-item">
                        <h4>Top Leaders</h4>
                        <div class="img-container">
                            <img src="top_leaders.png" alt="Top leaders">
                        </div>
                        <p>This chart shows the top 15 most traveled heads of government in the dataset.</p>
                    </div>
                    
                    <div class="grid-item">
                        <h4>Travel Between Regions</h4>
                        <div class="img-container">
                            <img src="region_flow_heatmap.png" alt="Region flow heatmap">
                        </div>
                        <p>This heatmap shows the flow of diplomatic travel between different regions, highlighting the most active regional relationships.</p>
                    </div>
                </div>
            </div>
            
            <div id="tab-comprehensive" class="tab-content">
                <h3>Comprehensive Trips Visualization</h3>
                <p>This visualization shows the top 15 countries in three categories: most visited countries, countries with the most diplomatic trips, and countries with the most diverse destinations. Use the dropdown menus to select categories and countries.</p>
                <iframe src="comprehensive_trips_viz.html"></iframe>
            </div>
            
            <div id="tab-country-pairs" class="tab-content">
                <h3>Country Pair Analysis</h3>
                <p>This visualization allows you to analyze diplomatic visits between specific country pairs over time. Use the dropdowns to select visiting and visited countries. You can select any combination of countries to see their diplomatic relationship over time.</p>
                <iframe src="country_pair_viz.html"></iframe>
            </div>
            
            <div id="tab-leader-timeline" class="tab-content">
                <h3>Leader Timeline Visualization</h3>
                <p>This visualization shows the diplomatic activity of the top 15 leaders over time. Use the dropdown to select specific leaders.</p>
                <iframe src="leader_timeline_viz.html"></iframe>
            </div>
            
            <div id="tab-diversity" class="tab-content">
                <h3>Diplomatic Diversity Visualization</h3>
                <p>This bubble chart visualization shows the diversity of diplomatic travel for top countries, with bubble size representing total trips and color representing the number of unique destinations visited.</p>
                <iframe src="diversity_viz.html"></iframe>
            </div>
        </div>
        
        <div class="section">
            <h2>Key Findings</h2>
            <ul>
                <li>The overall number of diplomatic trips has generally increased from 1990 to 2024, with notable fluctuations during global events.</li>
                <li>European countries dominate both as visitors and destinations, highlighting the density of diplomatic relations within Europe.</li>
                <li>Some countries show clear patterns of regional focus, while others display more global diplomatic engagement.</li>
                <li>Top leaders from major powers demonstrate the most consistent diplomatic travel activity over time.</li>
                <li>The United States, China, and major European powers are among the most frequently visited destinations.</li>
                <li>International organizations like the UN show distinctive travel patterns compared to individual countries.</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>Data Source: Country and Organization Leader Travel (COLT) dataset</p>
            <p>Frederick S. Pardee Institute for International Futures at the University of Denver</p>
            <p>Analysis date: March 2025</p>
        </div>
    </body>
    </html>
    """
    
    with open("colt_complete_dashboard.html", "w") as f:
        f.write(html_content)
    
    print("Complete dashboard created: colt_complete_dashboard.html")

# Execute all static visualizations
print("Creating static visualizations...")
for name, viz_func in tqdm(visualizations, desc="Creating static visualizations"):
    print(f"\nGenerating {name} visualization...")
    try:
        viz_func()
        print(f"✓ Successfully generated {name} visualization")
    except Exception as e:
        print(f"✗ Error generating {name} visualization: {str(e)}")

# Create interactive Plotly visualizations
print("\nCreating interactive visualizations...")
interactive_figs = [
    ("Comprehensive Trips Visualization", create_comprehensive_interactive_viz),
    ("Country Pair Visualization", create_country_pair_viz),
    ("Leader Timeline Visualization", create_leader_timeline),
    ("Diplomatic Diversity Visualization", create_diversity_viz)
]

for name, viz_func in tqdm(interactive_figs, desc="Creating interactive visualizations"):
    print(f"\nGenerating {name}...")
    try:
        fig = viz_func()
        print(f"✓ Successfully generated {name}")
    except Exception as e:
        print(f"✗ Error generating {name}: {str(e)}")
        print(f"Error details: {str(e)}")

# Create the comprehensive dashboard
create_complete_dashboard()

# Move all visualization files to the static folder
print("\nMoving visualization files to static folder...")
for file in os.listdir():
    if file.endswith('.png') or file.endswith('.html'):
        try:
            shutil.move(file, os.path.join('static', file))
            print(f"Moved {file} to static folder")
        except Exception as e:
            print(f"Error moving {file}: {str(e)}")

print("\nAnalysis complete! All visualizations created from the Country and Organization Leader Travel (COLT) dataset")
print("Frederick S. Pardee Institute for International Futures at the University of Denver")
