import time
import dht
from machine import Pin

# Initialize DHT22 sensor on digital pin D2
sensor = dht.DHT22(Pin(2))

print("timestamp_offset,temp_c,humidity_pct")

start_time = time.time()

while True:
    try:
        sensor.measure()
        temp_c = sensor.temperature()
        humidity = sensor.humidity()
        elapsed = time.time() - start_time
        
        # Send clean CSV data over USB Serial
        print(f"{elapsed},{temp_c:.2f},{humidity:.2f}")
        
    except OSError as e:
        print(f"ERROR: Sensor read failed - {e}")
        
    time.sleep(5)
