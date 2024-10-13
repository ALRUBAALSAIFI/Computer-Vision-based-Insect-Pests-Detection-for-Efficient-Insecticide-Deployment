# generate_reports.py

from load_data import load_data_from_csv, load_data_from_db
from setup_openai_api import generate_report

# Function to generate reports from data
def generate_reports_from_csv(csv_file):
    data = load_data_from_csv(csv_file)
    for index, row in data.iterrows():
        report = generate_report(row['pest_name'], row['location'], row['infection_level'], row['date'])
        print(f"\nReport for {row['pest_name']} in {row['location']}:")
        print(report)

# Function to generate reports from database
def generate_reports_from_db(db_file):
    data = load_data_from_db(db_file)
    for pest in data:
        pest_name, location, infection_level, date = pest
        report = generate_report(pest_name, location, infection_level, date)
        print(f"\nReport for {pest_name} in {location}:")
        print(report)
