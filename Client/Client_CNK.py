# Chamath Kulathilaka (100889193)
# TPRG 2131
# December 11, 2024
# This program is strictly my own work. Any material
# beyong course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to original author (s).
# This program sends 50 iterations of 5 vcgencmd commands to the server and exits
import os
import time
import socket
import json
import PySimpleGUI as sg

# Constants
#SERVER_HOST = '192.168.2.24'
SERVER_HOST = '127.0.0.1' # localhost
SERVER_PORT = 12345         # Port number
INTERVAL = 2                # Sampling interval in seconds
ITERATIONS = 50             # Number of data transmissions

# Function to get Pi vcgencmd data
def get_vcgen_data(iteration):
    """ The 6 vcgen commands are in here """
    core = float(os.popen('vcgencmd measure_temp').readline().split('=')[1].split("'")[0])
    v = float(os.popen('vcgencmd measure_volts ain1').readline().split('=')[1].split('V')[0])
    mem = float(os.popen('vcgencmd get_mem gpu').readline().split('=')[1].split("M")[0])
    arm = float(os.popen('vcgencmd get_mem arm').readline().split('=')[1].split("M")[0])
    clock = float(os.popen('vcgencmd measure_clock arm').readline().split('=')[1])
    try:
        data = {
            "core_temp": round(core, 1),  # core temperature
            "voltage": round(v, 1),  # Voltage
            "Memory": round(mem, 1),     # memory split for gpu
            "Arm-memory": round(arm, 1), # memory split for arm CPU
            "Core-speed": round(clock, 1),    # arm CPU core speed
            "iteration": iteration
        }
        return data
    except Exception as e:
        print(f"Error collecting data: {e}")
        return {}

# Main function for Client
def main():
    if os.name != 'posix':
        print("This script is designed to run on a Raspberry Pi. Exiting.")
        return
    client_socket = None
    window = None

    try:
        # Connect to server
        client_socket = socket.socket()
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")

        # Setup GUI
        layout = [
            [sg.Text("Connection Active", text_color="green", font=("Arial", 14))],
            [sg.Button("Exit", key="Exit", font=("Arial", 12))]
        ]
        window = sg.Window("Client Connection", layout, finalize=True)

        # Send data
        for i in range(1, ITERATIONS + 1):
            data = get_vcgen_data(i)
            json_data = json.dumps(data)
            client_socket.sendall(json_data.encode('utf-8'))
            time.sleep(INTERVAL)

            event, _ = window.read(timeout=10)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

        print("Data transmission complete. Exiting.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if client_socket:
            try:
                client_socket.close()
                print("Connection closed.")
            except Exception as e:
                print(f"Error closing socket: {e}")
        if window:
            window.close()


if __name__ == "__main__":
    main()