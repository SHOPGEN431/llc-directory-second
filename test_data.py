import pandas as pd
import re

def generate_seo_url(text):
    """Generate SEO-friendly URL from text"""
    url = re.sub(r'[^a-zA-Z0-9\s-]', '', str(text))
    url = re.sub(r'\s+', '-', url.strip())
    return url.lower()

# Load the CSV data
df = pd.read_csv(r'C:\Users\webd5\Downloads\LLC Data.csv')

# Clean and process data
df = df.fillna('')

# Get unique states and cities (filter out empty values)
states = sorted([state for state in df['state'].dropna().unique() if state and state.strip()])
cities = sorted([city for city in df['city'].dropna().unique() if city and city.strip()])

print("=== LLC Directory Data Analysis ===")
print(f"Total records: {len(df)}")
print(f"Unique states: {len(states)}")
print(f"Unique cities: {len(cities)}")

print("\n=== Sample States ===")
for i, state in enumerate(states[:10]):
    state_count = len(df[df['state'] == state])
    print(f"{i+1:2d}. {state} ({state_count} businesses)")

print("\n=== Sample Cities ===")
for i, city in enumerate(cities[:10]):
    city_count = len(df[df['city'] == city])
    print(f"{i+1:2d}. {city} ({city_count} businesses)")

print("\n=== Sample State-City Combinations ===")
sample_states = states[:3]
for state in sample_states:
    cities_in_state = sorted([city for city in df[df['state'] == state]['city'].dropna().unique() if city and city.strip()])
    print(f"\n{state}:")
    for city in cities_in_state[:5]:
        count = len(df[(df['state'] == state) & (df['city'] == city)])
        seo_url = generate_seo_url(city)
        print(f"  - {city} ({count} businesses) -> /state/{generate_seo_url(state)}/{seo_url}")

print("\n=== Data Quality Check ===")
print(f"Records with state: {len(df[df['state'].str.strip() != ''])}")
print(f"Records with city: {len(df[df['city'].str.strip() != ''])}")
print(f"Records with both state and city: {len(df[(df['state'].str.strip() != '') & (df['city'].str.strip() != '')])}")
