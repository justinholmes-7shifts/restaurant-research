import pandas as pd
import random

# Set random seed for reproducibility
random.seed(42)

# Load the research priority list
df = pd.read_csv('research_priority_list.csv')

print(f"Total restaurants in priority list: {len(df)}")

# Randomly sample 100 restaurants
sample_df = df.sample(n=100, random_state=42)

# Save to new CSV
sample_df.to_csv('random_100_sample.csv', index=False)

print(f"\nRandomly selected 100 restaurants and saved to random_100_sample.csv")
print(f"\nFirst 5 samples:")
print(sample_df[['name', 'address', 'contact_name', 'email']].head())
