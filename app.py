from flask import Flask, render_template, request, jsonify, send_from_directory
import pandas as pd
import os
import json
from datetime import datetime
import re

app = Flask(__name__)

# Global variable to store LLC data
llc_data = None

def load_llc_data(csv_file=r'C:\Users\webd5\Downloads\LLC Data.csv'):
    """Load LLC data from CSV file"""
    global llc_data
    try:
        if os.path.exists(csv_file):
            llc_data = pd.read_csv(csv_file)
            # Clean and process data
            llc_data = llc_data.fillna('')
            
            # Standardize state names (convert abbreviations to full names)
            state_mapping = {
                'AZ': 'Arizona',
                'CA': 'California',
                'CO': 'Colorado',
                'CT': 'Connecticut',
                'FL': 'Florida',
                'GA': 'Georgia',
                'IL': 'Illinois',
                'IN': 'Indiana',
                'KS': 'Kansas',
                'KY': 'Kentucky',
                'LA': 'Louisiana',
                'MA': 'Massachusetts',
                'MD': 'Maryland',
                'MI': 'Michigan',
                'MN': 'Minnesota',
                'MO': 'Missouri',
                'MS': 'Mississippi',
                'MT': 'Montana',
                'NC': 'North Carolina',
                'ND': 'North Dakota',
                'NE': 'Nebraska',
                'NH': 'New Hampshire',
                'NJ': 'New Jersey',
                'NM': 'New Mexico',
                'NV': 'Nevada',
                'NY': 'New York',
                'OH': 'Ohio',
                'OK': 'Oklahoma',
                'OR': 'Oregon',
                'PA': 'Pennsylvania',
                'RI': 'Rhode Island',
                'SC': 'South Carolina',
                'SD': 'South Dakota',
                'TN': 'Tennessee',
                'TX': 'Texas',
                'UT': 'Utah',
                'VA': 'Virginia',
                'VT': 'Vermont',
                'WA': 'Washington',
                'WI': 'Wisconsin',
                'WV': 'West Virginia',
                'WY': 'Wyoming',
                'AL': 'Alabama',
                'AK': 'Alaska',
                'AR': 'Arkansas',
                'DE': 'Delaware',
                'HI': 'Hawaii',
                'IA': 'Iowa',
                'ID': 'Idaho',
                'ME': 'Maine',
                'NV': 'Nevada'
            }
            
            # Apply state name standardization
            llc_data['state'] = llc_data['state'].replace(state_mapping)
            
            # Clean the 'about' field to remove accessibility/planning data
            def clean_about_field(about_text):
                if pd.isna(about_text) or about_text == '':
                    return ''
                try:
                    # Try to parse as JSON
                    import json
                    about_dict = json.loads(about_text)
                    # Remove Accessibility and Planning keys if they exist
                    if 'Accessibility' in about_dict:
                        del about_dict['Accessibility']
                    if 'Planning' in about_dict:
                        del about_dict['Planning']
                    # If the dict is now empty, return empty string
                    if not about_dict:
                        return ''
                    # Convert back to string, but only if there's meaningful content
                    return str(about_dict) if about_dict else ''
                except (json.JSONDecodeError, TypeError):
                    # If it's not valid JSON, return as is
                    return str(about_text)
            
            # Apply the cleaning function to the 'about' column
            llc_data['about'] = llc_data['about'].apply(clean_about_field)
            
            print(f"Loaded {len(llc_data)} LLC records")
            return True
        else:
            print(f"CSV file not found: {csv_file}")
            return False
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        return False

def generate_seo_url(text):
    """Generate SEO-friendly URL from text"""
    # Remove special characters and convert to lowercase
    url = re.sub(r'[^a-zA-Z0-9\s-]', '', str(text))
    url = re.sub(r'\s+', '-', url.strip())
    return url.lower()

def get_unique_states():
    """Get unique states from the data, sorted by business count (most populous first)"""
    if llc_data is None:
        return []
    # Use 'state' column and filter out empty values
    state_counts = llc_data['state'].value_counts()
    # Filter out empty values and sort by count (descending)
    states = state_counts[state_counts.index.str.strip() != ''].index.tolist()
    return states

def get_unique_cities():
    """Get unique cities from the data, sorted by business count (most populous first)"""
    if llc_data is None:
        return []
    # Use 'city' column and filter out empty values
    city_counts = llc_data['city'].value_counts()
    # Filter out empty values and sort by count (descending)
    cities = city_counts[city_counts.index.str.strip() != ''].index.tolist()
    return cities

def get_cities_with_states():
    """Get cities with their states for navigation, sorted by business count (most populous first)"""
    if llc_data is None:
        return []
    # Get unique city-state combinations with business counts
    city_state_counts = llc_data.groupby(['city', 'state']).size().reset_index(name='count')
    # Filter out empty values
    city_state_counts = city_state_counts[
        (city_state_counts['city'].str.strip() != '') & 
        (city_state_counts['state'].str.strip() != '')
    ]
    # Sort by count (descending) and convert to list of dictionaries
    cities_with_states = city_state_counts.sort_values('count', ascending=False).to_dict('records')
    return cities_with_states

def get_businesses_by_state(state):
    """Get businesses filtered by state"""
    if llc_data is None:
        return []
    # Filter by state column and handle case-insensitive matching
    filtered_data = llc_data[llc_data['state'].str.lower() == state.lower()]
    return filtered_data.to_dict('records')

def get_businesses_by_city(city):
    """Get businesses filtered by city"""
    if llc_data is None:
        return []
    # Filter by city column and handle case-insensitive matching
    filtered_data = llc_data[llc_data['city'].str.lower() == city.lower()]
    return filtered_data.to_dict('records')

def get_businesses_by_state_and_city(state, city):
    """Get businesses filtered by both state and city"""
    if llc_data is None:
        return []
    # Filter by both state and city columns
    filtered_data = llc_data[
        (llc_data['state'].str.lower() == state.lower()) & 
        (llc_data['city'].str.lower() == city.lower())
    ]
    return filtered_data.to_dict('records')

@app.route('/')
def index():
    """Homepage with search and filter functionality"""
    if llc_data is None:
        return render_template('index.html', llcs=[], total_count=0, states=[], cities=[])
    
    # Get search parameters
    search = request.args.get('search', '').lower()
    city = request.args.get('city', '')
    state = request.args.get('state', '')
    category = request.args.get('category', '')
    
    # Filter data
    filtered_data = llc_data.copy()
    
    if search:
        filtered_data = filtered_data[
            filtered_data['name'].str.lower().str.contains(search, na=False) |
            filtered_data['category'].str.lower().str.contains(search, na=False) |
            filtered_data['city'].str.lower().str.contains(search, na=False)
        ]
    
    if city:
        filtered_data = filtered_data[filtered_data['city'].str.lower() == city.lower()]
    
    if state:
        filtered_data = filtered_data[filtered_data['state'].str.lower() == state.lower()]
    
    if category:
        filtered_data = filtered_data[filtered_data['category'].str.lower().str.contains(category.lower(), na=False)]
    
    # Get unique values for filters
    states = get_unique_states()
    cities = get_unique_cities()
    categories = sorted(llc_data['category'].dropna().unique()) if 'category' in llc_data.columns else []
    
    return render_template('index.html', 
                         llcs=filtered_data.head(50).to_dict('records'),  # Limit to 50 for performance
                         total_count=len(filtered_data),
                         states=states,
                         cities=cities,
                         categories=categories,
                         search=search,
                         selected_city=city,
                         selected_state=state,
                         selected_category=category,
                         all_cities=get_cities_with_states())

@app.route('/state/<state_name>')
def state_page(state_name):
    """State page showing all businesses in a specific state"""
    if llc_data is None:
        return "State not found", 404
    
    # Find the actual state name from the URL
    state_data = None
    for state in get_unique_states():
        if generate_seo_url(state) == state_name:
            state_data = state
            break
    
    if not state_data:
        return "State not found", 404
    
    businesses = get_businesses_by_state(state_data)
    # Get cities in this specific state, sorted by business count (most populous first)
    state_data_filtered = llc_data[llc_data['state'] == state_data]
    city_counts = state_data_filtered['city'].value_counts()
    cities_in_state = city_counts[city_counts.index.str.strip() != ''].index.tolist()
    
    return render_template('state.html', 
                         state=state_data,
                         businesses=businesses,
                         cities=cities_in_state,
                         total_count=len(businesses),
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/state/<state_name>/<city_name>')
def city_page(state_name, city_name):
    """City page showing all businesses in a specific city"""
    if llc_data is None:
        return "City not found", 404
    
    # Find the actual state and city names from the URL
    state_data = None
    city_data = None
    
    for state in get_unique_states():
        if generate_seo_url(state) == state_name:
            state_data = state
            break
    
    if state_data:
        # Get cities in this state and find the matching one (sorted by business count)
        state_data_filtered = llc_data[llc_data['state'] == state_data]
        city_counts = state_data_filtered['city'].value_counts()
        cities_in_state = city_counts[city_counts.index.str.strip() != ''].index.tolist()
        for city in cities_in_state:
            if generate_seo_url(city) == city_name:
                city_data = city
                break
    
    if not state_data or not city_data:
        return "City not found", 404
    
    businesses = get_businesses_by_state_and_city(state_data, city_data)
    
    # Get cities in this specific state for the "Other Cities" section, sorted by business count
    state_data_filtered = llc_data[llc_data['state'] == state_data]
    city_counts = state_data_filtered['city'].value_counts()
    cities_in_state = city_counts[city_counts.index.str.strip() != ''].index.tolist()
    
    return render_template('city.html', 
                         state=state_data,
                         city=city_data,
                         businesses=businesses,
                         total_count=len(businesses),
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/api/search')
def api_search():
    """API endpoint for AJAX search"""
    if llc_data is None:
        return jsonify([])
    
    search = request.args.get('q', '').lower()
    if not search:
        return jsonify([])
    
    results = llc_data[
        llc_data['name'].str.lower().str.contains(search, na=False)
    ].head(10)
    
    return jsonify(results.to_dict('records'))

@app.route('/sitemap.xml')
def sitemap():
    """Generate XML sitemap for SEO"""
    if llc_data is None:
        return "No data available", 404
    
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add homepage
    sitemap += f'  <url>\n    <loc>{request.host_url}</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>\n'
    
    # Add state pages
    for state in get_unique_states():
        seo_url = generate_seo_url(state)
        sitemap += f'  <url>\n    <loc>{request.host_url}state/{seo_url}</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    
    # Add city pages
    for state in get_unique_states():
        # Get cities in this state sorted by business count
        state_data_filtered = llc_data[llc_data['state'] == state]
        city_counts = state_data_filtered['city'].value_counts()
        cities_in_state = city_counts[city_counts.index.str.strip() != ''].index.tolist()
        for city in cities_in_state:
            state_seo = generate_seo_url(state)
            city_seo = generate_seo_url(city)
            sitemap += f'  <url>\n    <loc>{request.host_url}state/{state_seo}/{city_seo}</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'
    
    sitemap += '</urlset>'
    
    return app.response_class(sitemap, mimetype='application/xml')

@app.route('/sitemap')
def html_sitemap():
    """Generate HTML sitemap for easy navigation"""
    if llc_data is None:
        return "No data available", 404
    
    states = get_unique_states()
    cities_with_states = get_cities_with_states()
    
    return render_template('sitemap.html', 
                         states=states,
                         cities_with_states=cities_with_states)

@app.route('/all-locations')
def all_locations():
    """Simple page listing all states and cities"""
    if llc_data is None:
        return "No data available", 404
    
    states = get_unique_states()
    cities_with_states = get_cities_with_states()
    
    return render_template('all_locations.html', 
                         states=states,
                         cities_with_states=cities_with_states)

@app.route('/about')
def about():
    """About Us page"""
    return render_template('about.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/contact')
def contact():
    """Contact Us page"""
    return render_template('contact.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/privacy')
def privacy():
    """Privacy Policy page"""
    return render_template('privacy.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/terms')
def terms():
    """Terms and Conditions page"""
    return render_template('terms.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/llc-guide')
def llc_guide():
    """LLC Formation Guide page"""
    return render_template('llc_guide.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/llc-vs-corp')
def llc_vs_corp():
    """LLC vs Corporation comparison page"""
    return render_template('llc_vs_corp.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/llc-tax-guide')
def llc_tax_guide():
    """LLC Tax Guide page"""
    return render_template('llc_tax_guide.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/llc-compliance')
def llc_compliance():
    """LLC Compliance page"""
    return render_template('llc_compliance.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/llc-glossary')
def llc_glossary():
    """LLC Glossary page"""
    return render_template('llc_glossary.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/llc-faq')
def llc_faq():
    """LLC FAQ page"""
    return render_template('llc_faq.html',
                         states=get_unique_states(),
                         all_cities=get_cities_with_states())

@app.route('/robots.txt')
def robots():
    """Generate robots.txt for SEO"""
    robots_content = f"""User-agent: *
Allow: /
Sitemap: {request.host_url}sitemap.xml
"""
    return app.response_class(robots_content, mimetype='text/plain')

if __name__ == '__main__':
    # Load data on startup
    load_llc_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
