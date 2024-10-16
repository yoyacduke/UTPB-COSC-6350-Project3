
import socket
import Crypto

# Constants
SERVER_HOST = '127.0.0.1'  # Change this to the server's IP if it's running on a different machine
SERVER_PORT = 5555         # Port number for the TCP connection


# Function to connect to the server and send packets
def tcp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Connect to the server
            client_socket.connect((SERVER_HOST, SERVER_PORT))
            print(f"[INFO] Connected to {SERVER_HOST}:{SERVER_PORT}")

            # Send the packet
            print(f"[INFO] Sending: {}")
            client_socket.sendall(.encode('utf-8'))

            # Wait for acknowledgment
            ack = client_socket.recv(1024).decode('utf-8')
            print(f"[INFO] Received acknowledgment: {ack}")

            # Close the connection (initiate the FIN/ACK handshake)
            print(f"[INFO] Initiating connection close.")
            client_socket.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(f"[ERROR] An error occurred: {e}")
        finally:
            print(f"[INFO] Connection closed.")


if __name__ == "__main__":
    tcp_client()
