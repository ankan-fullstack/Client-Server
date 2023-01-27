import socket
import time
import threading
import os
import psutil

def check_system_usage():
    load1, load5, load15 = psutil.getloadavg()
    cpu_usage = round((load15/os.cpu_count()) * 100, 2)
    ram_usage = psutil.virtual_memory()[2]
    return cpu_usage, ram_usage

def send_status(client_socket):
    while True:
        system = check_system_usage()
        message = f'CPU: {system[0]}, RAM: {system[1]}'
        client_socket.send(message.encode())
        time.sleep(5)

def client_program():
    host = socket.gethostbyname(socket.gethostname()+'.local')
    port = 5000

    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # instantiate
    client_socket.connect((host, port))  # connect to the server
    
    thread = threading.Thread(target=send_status, args=(client_socket,))
    thread.start()

        


if __name__ == '__main__':
    client_program()