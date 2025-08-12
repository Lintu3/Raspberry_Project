import time
import paho.mqtt.client as mqtt
from nordpool import elspot
from datetime import datetime, date

broker = "192.168.1.102"
topic = "oled/display"

def send_message(message):
    client = mqtt.Client()
    client.connect(broker, 1883, 60)
    client.publish(topic, message)
    client.disconnect()

def get_spot_price():
    prices = elspot.Prices("EUR")
    try:
        # Always fetch for today, area FI, hourly resolution(default)
        data = prices.fetch(
            end_date=date.today(),
            areas=["FI"],
            #default resolution is 60min
        )
    except Exception as e:
        print("Error fetching price:", e)
        return "Price fetch error"

    # Check if data is available and contains the expected structure
    if not data or "areas" not in data or "FI" not in data["areas"]:
        print("No data or missing FI area:", data)
        return "No price data"

    now = datetime.now()
    # Find the current hour's price
    for entry in data["areas"]["FI"]["values"]:
        if entry["start"].hour == now.hour and entry["start"].date() == now.date():
            price_eur_mwh = entry["value"]  # EUR/MWh
            price_cents_kwh = price_eur_mwh / 10  # EUR/MWh to c/kWh
            return f" {price_cents_kwh:.2f} c/kWh"
    return "Price not found"

if __name__ == "__main__":
    while True:
        msg = get_spot_price()
        send_message(msg)
        print("Sent:", msg)
        time.sleep(3600)  # Wait 1 hour