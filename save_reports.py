# save_reports.py

# Function to save reports to a file
def save_reports_to_file(reports, file_name):
    with open(file_name, 'w') as f:
        for report in reports:
            f.write(report + "\n")
    print(f"Reports saved to {file_name}")

# Function to save reports to database
def save_reports_to_db(reports, db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    for report in reports:
        cursor.execute("INSERT INTO reports (report) VALUES (?)", (report,))
    conn.commit()
    conn.close()
    print(f"Reports saved to {db_file} database")
