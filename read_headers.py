import pandas as pd

# Read the CSV file
df = pd.read_csv(r'C:\Users\webd5\Downloads\LLC Data.csv')

# Get all headers
headers = df.columns.tolist()

print('Complete CSV Headers:')
print('=' * 60)

for i, header in enumerate(headers):
    print(f'{i+1:2d}. {header}')

print(f'\nTotal columns: {len(headers)}')


