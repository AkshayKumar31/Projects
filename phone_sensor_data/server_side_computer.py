# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 11:52:20 2023

@author: aksha
"""

import socket

HOST = '0.0.0.0'
PORT = 8000

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f"Listening on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            print(f"Connected by {addr}")

            try:
                data = conn.recv(1024)
                if not data:
                    break

                # Process the received data here
                print(f"Received data: {data}")

            except Exception as e:
                print(f"Error while handling connection: {e}")

if __name__ == '__main__':
    main()