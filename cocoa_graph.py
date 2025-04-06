import pandas as pd
import matplotlib.pyplot as plt
from app import hello_world

# Load the cocoa exports data from the CSV file.
# Assumption: the CSV file contains columns 'Year' and 'Export_Value'
# If your CSV uses different column names, update them accordingly.

cocoa = pd.read_csv('Hackathon Data/Cocoa & Cocoa Prod..csv')
# Verify required columns exist
if 'Year' not in cocoa.columns or 'Export_Value' not in cocoa.columns:
    raise ValueError("The CSV file must contain 'Year' and 'Export_Value' columns.")
 
# Convert the Year column to numeric (in case it's read as string) and sort the data.
cocoa['Year'] = pd.to_numeric(cocoa['Year'], errors='coerce')
cocoa.sort_values('Year', inplace=True)

# Plot the line graph for cocoa exports trend.
plt.figure(figsize=(10, 6))
plt.plot(cocoa['Year'], cocoa['Export_Value'], marker='o', linestyle='-', label='Cocoa Exports')
plt.title("Trend in Cocoa Exports")
plt.xlabel("Year")
plt.ylabel("Export Value")
plt.legend()
plt.tight_layout()

# Save the graph as an image file if needed
plt.savefig("cocoa_exports_trend.png")

# Display the plot
plt.show()