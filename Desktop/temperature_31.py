import os
from datetime import datetime
import mysql.connector

# fetch database settings from environment variables
db = mysql.connector.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    database=os.environ.get("DB_NAME")
)
# create a cursor to interact with the database
cursor = db.cursor()

# get data from the database
cursor.execute("SELECT * FROM sensei_data WHERE temperature >= 31")
result = cursor.fetchall()

# Save results to a readable file
with open("temperature_report.txt", "w", encoding="utf-8") as f:
    f.write("Timestamp              | Temperature (°C)\n")
    f.write("-----------------------+-----------------\n")
    for row in result:
        timestamp = row[1]
        temperature = row[2]
        if isinstance(timestamp, datetime):
            time = timestamp.strftime("%d.%m.%Y %H:%M:%S")
        else:
            time = str(timestamp)
        f.write(f"{time:21} | {temperature:.1f}°C\n")
        print(f"Timestamp: {time}, Temperature: {temperature:.1f}°C")

print("Report saved to temperature_report.txt")
# Close the connection
db.close()

#Four days and 19 hours temperature 31 or more