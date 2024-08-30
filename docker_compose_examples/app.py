import socket
import sys
import time

def communicate(name, target_port, listen_port):
    message = f"Hello from {name}"
    goodbye_message = f"Goodbye from {name}"
    buffer_size = 1024

    # Try to send a message first
    connected = False
    for _ in range(5):  # Retry connecting for a few times
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(("app", target_port))
                print(f"{name} sending: {message}")
                s.sendall(message.encode())
                connected = True

                data = s.recv(buffer_size)
                print(f"{name} received: {data.decode()}")

                print(f"{name} sending: {goodbye_message}")
                s.sendall(goodbye_message.encode())
                break  # Exit the loop once message is sent
        except ConnectionRefusedError:
            print(f"{name} waiting to connect...")
            time.sleep(5)  # Wait a bit for the other service to be up

    # If sending first didn't work, listen for a message
    if not connected:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_listen:
            s_listen.bind(("0.0.0.0", listen_port))
            s_listen.listen(1)
            print(f"{name} is now listening on port {listen_port}")
            conn, addr = s_listen.accept()
            with conn:
                data = conn.recv(buffer_size)
                print(f"{name} received: {data.decode()}")
                print(f"{name} sending: {message}")
                conn.sendall(message.encode())

                data = conn.recv(buffer_size)
                print(f"{name} received: {data.decode()}")

if __name__ == "__main__":
    name = sys.argv[1]
    target_port = int(sys.argv[2])
    listen_port = int(sys.argv[3])
    communicate(name, target_port, listen_port)