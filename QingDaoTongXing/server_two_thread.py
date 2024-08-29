import socket
import threading

def receive_messages(server_socket):
    while True:
        client, addr = server_socket.accept()
        print(f"Accepted connection from: {addr}")

        while True:
            received_message = client.recv(1024)
            if not received_message:
                break
            print(f"Received: {received_message.decode()}")

        client.close()

def send_messages(server_socket):
    client, addr = server_socket.accept()
    print(f"Accepted connection from: {addr}")

    while True:
        message = input("Enter message to send (type 'quit' to exit): ")
        if message.lower() == 'quit':
            break
        client.send(message.encode())

    client.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.4.100', 8882))
    server.listen(1)#最多监听几个客户端
    print("Server listening on port 8882...")

    receive_thread = threading.Thread(target=receive_messages, args=(server,))
    send_thread = threading.Thread(target=send_messages, args=(server,))

    receive_thread.start()
    send_thread.start()

if __name__ == "__main__":
    main()