import pandas as pd

# State mapping dictionary
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
    'ME': 'Maine'
}

# Load the CSV data
df = pd.read_csv(r'C:\Users\webd5\Downloads\LLC Data.csv')

# Clean and process data
df = df.fillna('')

print("=== Before State Standardization ===")
print("Sample states found in data:")
states_before = df['state'].dropna().unique()
for state in sorted(states_before)[:10]:
    count = len(df[df['state'] == state])
    print(f"  {state} ({count} businesses)")

# Apply state name standardization
df['state'] = df['state'].replace(state_mapping)

print("\n=== After State Standardization ===")
print("Sample states after standardization:")
states_after = df['state'].dropna().unique()
for state in sorted(states_after)[:10]:
    count = len(df[df['state'] == state])
    print(f"  {state} ({count} businesses)")

print(f"\n=== Summary ===")
print(f"Total records: {len(df)}")
print(f"Unique states before: {len(states_before)}")
print(f"Unique states after: {len(states_after)}")

# Show some examples of the conversion
print(f"\n=== State Name Conversion Examples ===")
for abbrev, full_name in list(state_mapping.items())[:10]:
    before_count = len(df[df['state'] == abbrev])
    after_count = len(df[df['state'] == full_name])
    if before_count > 0 or after_count > 0:
        print(f"  {abbrev} -> {full_name} (before: {before_count}, after: {after_count})")
