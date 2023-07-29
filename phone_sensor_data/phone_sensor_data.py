# Python script using QPython 

import androidhelper as android
import json
import socket
import time

droid = android.Android()
droid.startSensingTimed(1, 255)
print("gps locating")
droid.startLocating()
print("reading GPS")
event = droid.eventWaitFor('location', 10000).result
print(event)
time.sleep(2)
# Set up socket connection
HOST = '{your computers ip address on the used network}'
PORT = 8000

def get_sensor_data():
    # Get sensor readings from Android
    accelerometer_data = droid.sensorsReadAccelerometer().result
    magnetometer_data = droid.sensorsReadMagnetometer().result
    orientation_data = droid.sensorsReadOrientation().result
    gps_data = droid.readLocation().result

    # Package data into a dictionary
    sensor_data = {
        'accelerometer': accelerometer_data,
        'magnetometer': magnetometer_data,
        'orientation': orientation_data,
        'gps': gps_data
    }
    #print(sensor_data)

    return json.dumps(sensor_data)

def send_data_to_server(data):
    try:
        # Create a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            # Send data to the server
            client_socket.sendall(data.encode())
    except Exception as e:
        print(f"Error while sending data: {e}")

def main():
    try:
        while True:
            sensor_data = get_sensor_data()
            print(sensor_data)
            send_data_to_server(sensor_data)
            time.sleep(1)  # Adjust the sleep duration to control data transmission frequency
    except KeyboardInterrupt:
        print("Data transmission stopped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()