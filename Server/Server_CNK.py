# Chamath Kulathilaka (100889193)
# TPRG 2131
# December 11, 2024
# This program is strictly my own work. Any material
# beyong course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to original author (s).
# This program is a server that will show 6 values obtained from the Json object sent by the client.
import os
import time
import socket
import json
import PySimpleGUI as sg

# Server constants
#HOST = "192.168.2.24"
HOST = "127.0.0.1" #Local host
PORT = 12345

# Main server logic
def start_server():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"Server listening on {HOST}:{PORT}")

    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    # Setup GUI
    layout = [
        [sg.Text("Waiting for data...", size=(30, 1), key=f"Data{i}", font=("Arial", 12))] for i in range(6)
    ] + [[sg.Button("Exit", font=("Arial", 12))] + [sg.Text("LED Status: ", size=(6, 1), font=("Arial", 12)), sg.Text("\u1F4A1", key="LED", font=("Arial",12))]]

    window = sg.Window("Server Data Viewer", layout, finalize=True)

    try:
        while True:
            event, _ = window.read(timeout=100)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            data = conn.recv(1024)
            if not data:
                break

            data_dict = json.loads(data.decode('utf-8'))
            for i, (key, value) in enumerate(data_dict.items()):
                if i < 6:
                    window[f"Data{i}"].update(f"{key}: {value}")
                    
            window["LED"].update("\u1F7E2") #Update LED to ON
            time.sleep(1)
            window["LED"].update("\u1F534")

    except Exception as e:
        print(f"Error receiving data: {e}")

    finally:
        conn.close()
        server_socket.close()
        window.close()

if __name__ == "__main__":
    start_server()
