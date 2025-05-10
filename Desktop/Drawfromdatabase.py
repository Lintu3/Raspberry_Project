import mysql.connector
import matplotlib.pyplot as plt

# MariaDB
db = mysql.connector.connect(
    host="00.00.00.00",  # database IP address
    user="yyyy",               # database user
    password="????",        # password
    database="xxxx"            # database
)

cursor = db.cursor()

# get data
cursor.execute("SELECT timestamp, temperature, humidity, soilmoisture FROM xxxx")
result = cursor.fetchall()
db.close()

# separate data
timestamps = [row[0] for row in result]
temperatures = [row[1] for row in result]
humidities = [row[2] for row in result]
soilmoisture = [row[3] for row in result]

# draw
fig, ax1 = plt.subplots(figsize=(12, 6))

# Temperature to left Y-axis
color = 'tab:red'
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Temperature (°C)', color=color)
ax1.plot(timestamps, temperatures, color=color, label='Temperature (°C)')
ax1.tick_params(axis='y', labelcolor=color)

# Moisture and humidity % to right Y-axis
ax2 = ax1.twinx()  
color1 = 'tab:blue'
color2 = 'tab:green'
ax2.set_ylabel('Humidity and Soilmoisture (%)', color=color2)
ax2.plot(timestamps, humidities, color=color1, label='Humidity (%)')
ax2.plot(timestamps, soilmoisture, color=color2, label='Soilmoisture (%)')
ax2.tick_params(axis='y', labelcolor=color2)

#Legend and header
fig.suptitle('Arduino Data')
fig.tight_layout()  # make sure they fit
fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.93))

plt.show()
