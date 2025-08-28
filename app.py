from flask import Flask, render_template, request, jsonify, send_from_directory, redirect, url_for
import pandas as pd
import os
import json
from datetime import datetime
import re
from urllib.parse import quote_plus
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Global variable to store LLC data
llc_data = None
states_data = None

def load_llc_data(csv_file='C:/llc-formation-website/LLC Data.csv'):
    """Load LLC data from CSV file"""
    global llc_data
    try:
        if os.path.exists(csv_file):
            llc_data = pd.read_csv(csv_file)
            # Clean and process data
            llc_data = llc_data.fillna('')
            # Filter for business data (remove rows with empty business names)
            llc_data = llc_data[llc_data['name'].notna() & (llc_data['name'] != '')]
            print(f"Loaded {len(llc_data)} business records")
            return True
        else:
            print(f"CSV file not found: {csv_file}")
            return False
    except Exception as e:
        print(f"Error loading CSV data: {e}")
        return False

def load_states_data():
    """Load states data for SEO pages"""
    global states_data
    states_data = {
        'alabama': {'name': 'Alabama', 'abbr': 'AL', 'formation_fee': 200, 'annual_fee': 100},
        'alaska': {'name': 'Alaska', 'abbr': 'AK', 'formation_fee': 250, 'annual_fee': 100},
        'arizona': {'name': 'Arizona', 'abbr': 'AZ', 'formation_fee': 50, 'annual_fee': 0},
        'arkansas': {'name': 'Arkansas', 'abbr': 'AR', 'formation_fee': 45, 'annual_fee': 150},
        'california': {'name': 'California', 'abbr': 'CA', 'formation_fee': 70, 'annual_fee': 800},
        'colorado': {'name': 'Colorado', 'abbr': 'CO', 'formation_fee': 50, 'annual_fee': 10},
        'connecticut': {'name': 'Connecticut', 'abbr': 'CT', 'formation_fee': 120, 'annual_fee': 80},
        'delaware': {'name': 'Delaware', 'abbr': 'DE', 'formation_fee': 90, 'annual_fee': 300},
        'florida': {'name': 'Florida', 'abbr': 'FL', 'formation_fee': 125, 'annual_fee': 138.75},
        'georgia': {'name': 'Georgia', 'abbr': 'GA', 'formation_fee': 100, 'annual_fee': 50},
        'hawaii': {'name': 'Hawaii', 'abbr': 'HI', 'formation_fee': 50, 'annual_fee': 15},
        'idaho': {'name': 'Idaho', 'abbr': 'ID', 'formation_fee': 100, 'annual_fee': 0},
        'illinois': {'name': 'Illinois', 'abbr': 'IL', 'formation_fee': 150, 'annual_fee': 75},
        'indiana': {'name': 'Indiana', 'abbr': 'IN', 'formation_fee': 90, 'annual_fee': 30},
        'iowa': {'name': 'Iowa', 'abbr': 'IA', 'formation_fee': 50, 'annual_fee': 30},
        'kansas': {'name': 'Kansas', 'abbr': 'KS', 'formation_fee': 90, 'annual_fee': 55},
        'kentucky': {'name': 'Kentucky', 'abbr': 'KY', 'formation_fee': 40, 'annual_fee': 15},
        'louisiana': {'name': 'Louisiana', 'abbr': 'LA', 'formation_fee': 100, 'annual_fee': 25},
        'maine': {'name': 'Maine', 'abbr': 'ME', 'formation_fee': 175, 'annual_fee': 85},
        'maryland': {'name': 'Maryland', 'abbr': 'MD', 'formation_fee': 100, 'annual_fee': 300},
        'massachusetts': {'name': 'Massachusetts', 'abbr': 'MA', 'formation_fee': 500, 'annual_fee': 500},
        'michigan': {'name': 'Michigan', 'abbr': 'MI', 'formation_fee': 50, 'annual_fee': 25},
        'minnesota': {'name': 'Minnesota', 'abbr': 'MN', 'formation_fee': 155, 'annual_fee': 0},
        'mississippi': {'name': 'Mississippi', 'abbr': 'MS', 'formation_fee': 50, 'annual_fee': 25},
        'missouri': {'name': 'Missouri', 'abbr': 'MO', 'formation_fee': 50, 'annual_fee': 0},
        'montana': {'name': 'Montana', 'abbr': 'MT', 'formation_fee': 70, 'annual_fee': 20},
        'nebraska': {'name': 'Nebraska', 'abbr': 'NE', 'formation_fee': 100, 'annual_fee': 10},
        'nevada': {'name': 'Nevada', 'abbr': 'NV', 'formation_fee': 75, 'annual_fee': 350},
        'new-hampshire': {'name': 'New Hampshire', 'abbr': 'NH', 'formation_fee': 100, 'annual_fee': 100},
        'new-jersey': {'name': 'New Jersey', 'abbr': 'NJ', 'formation_fee': 125, 'annual_fee': 75},
        'new-mexico': {'name': 'New Mexico', 'abbr': 'NM', 'formation_fee': 50, 'annual_fee': 0},
        'new-york': {'name': 'New York', 'abbr': 'NY', 'formation_fee': 200, 'annual_fee': 9},
        'north-carolina': {'name': 'North Carolina', 'abbr': 'NC', 'formation_fee': 125, 'annual_fee': 200},
        'north-dakota': {'name': 'North Dakota', 'abbr': 'ND', 'formation_fee': 135, 'annual_fee': 50},
        'ohio': {'name': 'Ohio', 'abbr': 'OH', 'formation_fee': 99, 'annual_fee': 0},
        'oklahoma': {'name': 'Oklahoma', 'abbr': 'OK', 'formation_fee': 100, 'annual_fee': 25},
        'oregon': {'name': 'Oregon', 'abbr': 'OR', 'formation_fee': 100, 'annual_fee': 100},
        'pennsylvania': {'name': 'Pennsylvania', 'abbr': 'PA', 'formation_fee': 125, 'annual_fee': 70},
        'rhode-island': {'name': 'Rhode Island', 'abbr': 'RI', 'formation_fee': 150, 'annual_fee': 50},
        'south-carolina': {'name': 'South Carolina', 'abbr': 'SC', 'formation_fee': 110, 'annual_fee': 0},
        'south-dakota': {'name': 'South Dakota', 'abbr': 'SD', 'formation_fee': 150, 'annual_fee': 50},
        'tennessee': {'name': 'Tennessee', 'abbr': 'TN', 'formation_fee': 300, 'annual_fee': 300},
        'texas': {'name': 'Texas', 'abbr': 'TX', 'formation_fee': 300, 'annual_fee': 0},
        'utah': {'name': 'Utah', 'abbr': 'UT', 'formation_fee': 70, 'annual_fee': 20},
        'vermont': {'name': 'Vermont', 'abbr': 'VT', 'formation_fee': 125, 'annual_fee': 0},
        'virginia': {'name': 'Virginia', 'abbr': 'VA', 'formation_fee': 100, 'annual_fee': 50},
        'washington': {'name': 'Washington', 'abbr': 'WA', 'formation_fee': 200, 'annual_fee': 60},
        'west-virginia': {'name': 'West Virginia', 'abbr': 'WV', 'formation_fee': 100, 'annual_fee': 25},
        'wisconsin': {'name': 'Wisconsin', 'abbr': 'WI', 'formation_fee': 130, 'annual_fee': 25},
        'wyoming': {'name': 'Wyoming', 'abbr': 'WY', 'formation_fee': 100, 'annual_fee': 50}
    }

def generate_seo_url(text):
    """Generate SEO-friendly URL from text"""
    url = re.sub(r'[^a-zA-Z0-9\s-]', '', text)
    url = re.sub(r'\s+', '-', url.strip())
    return url.lower()

def generate_meta_description(content, max_length=160):
    """Generate meta description for SEO"""
    description = re.sub(r'<[^>]+>', '', content)
    description = re.sub(r'\s+', ' ', description).strip()
    return description[:max_length] + "..." if len(description) > max_length else description

@app.route('/')
def index():
    """Homepage with comprehensive SEO"""
    return render_template('index.html', 
                         title="LLC Formation Services - Start Your Business Today",
                         meta_description="Professional LLC formation services. Form your LLC in any state with expert guidance, legal compliance, and ongoing support. Get started today!",
                         structured_data=get_homepage_structured_data())

@app.route('/llc-formation')
def llc_formation():
    """LLC Formation service page"""
    return render_template('llc_formation.html',
                         title="LLC Formation Services - Complete Business Setup",
                         meta_description="Complete LLC formation services including filing, compliance, and ongoing support. Expert guidance for starting your business right.",
                         structured_data=get_service_structured_data())

@app.route('/state/<state_slug>')
def state_llc_formation(state_slug):
    """State-specific LLC formation pages for SEO"""
    if state_slug not in states_data:
        return "State not found", 404
    
    state_info = states_data[state_slug]
    
    # Get businesses in this state
    if llc_data is not None:
        state_businesses = llc_data[
            (llc_data['state'].str.lower() == state_info['abbr'].lower()) |
            (llc_data['us_state'].str.lower() == state_info['abbr'].lower())
        ]
    else:
        state_businesses = pd.DataFrame()
    
    title = f"LLC Formation in {state_info['name']} - Start Your {state_info['abbr']} LLC"
    meta_description = f"Form your LLC in {state_info['name']} with our expert services. {state_info['name']} LLC formation fee: ${state_info['formation_fee']}. Get started today!"
    
    return render_template('state_llc.html',
                         state=state_info,
                         businesses=state_businesses.to_dict('records') if len(state_businesses) > 0 else [],
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_state_structured_data(state_info))

@app.route('/city/<state_slug>/<city_slug>')
def city_llc_formation(state_slug, city_slug):
    """City-specific LLC formation pages for SEO"""
    if state_slug not in states_data:
        return "State not found", 404
    
    state_info = states_data[state_slug]
    
    # Get businesses in this city
    if llc_data is not None:
        city_businesses = llc_data[
            (llc_data['state'].str.lower() == state_info['abbr'].lower()) |
            (llc_data['us_state'].str.lower() == state_info['abbr'].lower())
        ]
        city_businesses = city_businesses[
            city_businesses['city'].str.lower().str.replace(' ', '-') == city_slug.lower()
        ]
    else:
        city_businesses = pd.DataFrame()
    
    # Get city name from first business or use slug
    if len(city_businesses) > 0:
        city_name = city_businesses.iloc[0]['city']
    else:
        city_name = city_slug.replace('-', ' ').title()
    
    title = f"LLC Formation in {city_name}, {state_info['abbr']} - Start Your Business"
    meta_description = f"Form your LLC in {city_name}, {state_info['name']} with our expert services. Local business formation support in {city_name}. Get started today!"
    
    return render_template('city_llc.html',
                         state=state_info,
                         city_name=city_name,
                         city_slug=city_slug,
                         businesses=city_businesses.to_dict('records') if len(city_businesses) > 0 else [],
                         title=title,
                         meta_description=meta_description,
                         structured_data=get_city_structured_data(state_info, city_name))

@app.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html',
                         title="LLC Formation Pricing - Transparent Costs",
                         meta_description="Clear LLC formation pricing with no hidden fees. Compare our affordable packages and choose the best option for your business needs.",
                         states=states_data)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html',
                         title="About Our LLC Formation Services",
                         meta_description="Learn about our experienced team and commitment to helping entrepreneurs form their LLCs with confidence and legal compliance.")

@app.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html',
                         title="Contact Us - LLC Formation Support",
                         meta_description="Get in touch with our LLC formation experts. We're here to help you start your business with confidence and legal compliance.")

@app.route('/blog')
def blog():
    """Blog page"""
    return render_template('blog.html',
                         title="LLC Formation Blog - Expert Insights",
                         meta_description="Stay informed with the latest LLC formation tips, legal updates, and business advice from our expert team.")

@app.route('/sitemap.xml')
def sitemap():
    """Generate XML sitemap for SEO"""
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # Add static pages
    pages = [
        {'url': '/', 'priority': '1.0', 'changefreq': 'daily'},
        {'url': '/llc-formation', 'priority': '0.9', 'changefreq': 'weekly'},
        {'url': '/pricing', 'priority': '0.8', 'changefreq': 'weekly'},
        {'url': '/about', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/contact', 'priority': '0.7', 'changefreq': 'monthly'},
        {'url': '/blog', 'priority': '0.6', 'changefreq': 'weekly'}
    ]
    
    for page in pages:
        sitemap += f'  <url>\n    <loc>{request.host_url.rstrip("/")}{page["url"]}</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>{page["changefreq"]}</changefreq>\n    <priority>{page["priority"]}</priority>\n  </url>\n'
    
    # Add state pages
    for state_slug in states_data.keys():
        sitemap += f'  <url>\n    <loc>{request.host_url.rstrip("/")}/state/{state_slug}</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n'
    
    # Add city pages if we have LLC data
    if llc_data is not None:
        # Get unique city-state combinations
        city_states = llc_data[['city', 'state', 'us_state']].dropna().drop_duplicates()
        for _, row in city_states.iterrows():
            city = row['city']
            state_abbr = row['state'] if pd.notna(row['state']) else row['us_state']
            
            # Find matching state slug
            state_slug = None
            for slug, state_info in states_data.items():
                if state_info['abbr'].lower() == state_abbr.lower():
                    state_slug = slug
                    break
            
            if state_slug and city:
                city_slug = generate_seo_url(city)
                sitemap += f'  <url>\n    <loc>{request.host_url.rstrip("/")}/city/{state_slug}/{city_slug}</loc>\n    <lastmod>{datetime.now().strftime("%Y-%m-%d")}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n'
    
    sitemap += '</urlset>'
    
    return app.response_class(sitemap, mimetype='application/xml')

@app.route('/robots.txt')
def robots():
    """Generate robots.txt for SEO"""
    robots_content = f"""User-agent: *
Allow: /
Sitemap: {request.host_url}sitemap.xml

# Disallow admin areas
Disallow: /admin/
Disallow: /private/
"""
    return app.response_class(robots_content, mimetype='text/plain')

def get_homepage_structured_data():
    """Generate structured data for homepage"""
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "LLC Formation Services",
        "url": request.host_url,
        "logo": f"{request.host_url}static/images/logo.png",
        "description": "Professional LLC formation services for entrepreneurs and businesses",
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "US"
        },
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": "+1-800-LLC-FORM",
            "contactType": "customer service"
        },
        "sameAs": [
            "https://www.facebook.com/llcformationservices",
            "https://www.linkedin.com/company/llcformationservices"
        ]
    }

def get_service_structured_data():
    """Generate structured data for service page"""
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "LLC Formation Services",
        "description": "Complete LLC formation services including filing, compliance, and ongoing support",
        "provider": {
            "@type": "Organization",
            "name": "LLC Formation Services"
        },
        "areaServed": {
            "@type": "Country",
            "name": "United States"
        },
        "hasOfferCatalog": {
            "@type": "OfferCatalog",
            "name": "LLC Formation Packages",
            "itemListElement": [
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Basic LLC Formation"
                    }
                },
                {
                    "@type": "Offer",
                    "itemOffered": {
                        "@type": "Service",
                        "name": "Premium LLC Formation"
                    }
                }
            ]
        }
    }

def get_state_structured_data(state_info):
    """Generate structured data for state pages"""
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"LLC Formation in {state_info['name']}",
        "description": f"Form your LLC in {state_info['name']} with expert guidance and legal compliance",
        "provider": {
            "@type": "Organization",
            "name": "LLC Formation Services"
        },
        "areaServed": {
            "@type": "State",
            "name": state_info['name']
        },
        "offers": {
            "@type": "Offer",
            "price": str(state_info['formation_fee']),
            "priceCurrency": "USD",
            "description": f"LLC formation fee in {state_info['name']}"
        }
    }

def get_city_structured_data(state_info, city_name):
    """Generate structured data for city pages"""
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": f"LLC Formation in {city_name}, {state_info['name']}",
        "description": f"Form your LLC in {city_name}, {state_info['name']} with expert guidance and local business support",
        "provider": {
            "@type": "Organization",
            "name": "LLC Formation Services"
        },
        "areaServed": {
            "@type": "City",
            "name": city_name,
            "addressRegion": state_info['name'],
            "addressCountry": "US"
        },
        "offers": {
            "@type": "Offer",
            "price": str(state_info['formation_fee']),
            "priceCurrency": "USD",
            "description": f"LLC formation fee in {city_name}, {state_info['name']}"
        }
    }

if __name__ == '__main__':
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Load data on startup
    load_states_data()
    load_llc_data()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
