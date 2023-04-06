import requests
import pandas as pd
from bs4 import BeautifulSoup

# Define the Wikipedia page URL
url = 'https://ru.wikipedia.org/wiki/Список_субъектов_Российской_Федерации_по_валовому_продукту'

# Make a GET request to the page
response = requests.get(url)

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table with the class "wikitable sortable"
table = soup.find('table', {'class': 'wikitable sortable'})

# Parse the table data with Pandas
df = pd.read_html(str(table))[0]

# Save the table as a CSV file
csv_file_path = r'C:\Users\HOME\PycharmProjects\DA_ConstructionMarketplaces\vrp_2014_2018.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print('Table saved as', csv_file_path)