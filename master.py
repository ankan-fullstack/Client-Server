import socket
import threading
import time

host = socket.gethostbyname(socket.gethostname()+'.local')
port = 5000
addr = (host,port)
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(addr)

client_data = {}

def handle_client(conn, address):
    print("Connection from: " + str(address))
    while True:
        try: 
            data = conn.recv(1024).decode()
            if len(data)==0:
                continue
            client_data[address]['status'] = data
        except ConnectionResetError as e:
            print(e)

def health_check_probe():
    while True:
        for key in list(client_data):
            conn = client_data[key]['connection']
            try:
                conn.send(''.encode())
            except BrokenPipeError as e:
                del client_data[key]
        status = [(key, client_data[key]['status']) for key in client_data.keys()]
        print(f'[ACTIVE CONNECTIONS]: {len(client_data)}')
        print(status)
        time.sleep(10)


def server_program():
    print('[SERVER STARTED]: Starting the server.')
    server_socket.listen()
    print(f'[SERVER LISTENING]: Server listening on port {addr}')
    health_check_thread = threading.Thread(target=health_check_probe)
    health_check_thread.start()
    while True:
        conn, address = server_socket.accept()
        conn.settimeout(8.0)
        client_data[address] = {
            'connection': conn,
            'status': 'Not Updated Yet!'
        }
        thread = threading.Thread(target=handle_client, args=(conn, address))
        thread.start()


if __name__ == '__main__':
    server_program()