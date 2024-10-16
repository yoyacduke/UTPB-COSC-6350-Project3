import socket
from concurrent.futures import ThreadPoolExecutor
from Crypto import *

# Constants
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5555       # Port number
TIMEOUT = 600     # 10 minutes (in seconds)
MAX_THREADS = 10  # Maximum number of threads in the pool


# Function to handle client connection
def handle_client(conn, addr):
    conn.settimeout(TIMEOUT)
    print(f"[INFO] Connection from {addr} established.")
    try:
        while True:
            try:
                file_size = 0
                crumbs = []
                with open("risk.bmp", "rb") as dat_file:
                    dat_file.seek(0, 2)
                    file_size = dat_file.tell()
                    dat_file.seek(0)
                    for x in range(file_size):
                        for crumb in decompose_byte(dat_file.read(1)):
                            crumbs.append(crumb)

                # Wait for data from the client
                data = conn.recv(1024)
                if not data:
                    print(f"[INFO] Connection from {addr} closed by client.")
                    break

                if len(data) > 0:
                    print(f"[DATA] {data.decode('utf-8', errors='replace')}")

                    # Send an ACK (just acknowledge the data)
                    conn.sendall(b'ACK')
                else:
                    print(f"[WARN] Incomplete packet from {addr}.")
            except socket.timeout:
                print(f"[INFO] Connection from {addr} timed out.")
                break
    except Exception as e:
        print(f"[ERROR] Error handling client {addr}: {e}")
    finally:
        # Attempt to close connection via FIN/ACK method
        try:
            conn.shutdown(socket.SHUT_RDWR)
            conn.close()
        except Exception as e:
            print(f"[ERROR] Error closing connection from {addr}: {e}")
        print(f"[INFO] Connection from {addr} has been closed.")


# Main server function
def start_server():
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"[INFO] Server started, listening on {PORT}...")

            while True:
                conn, addr = server_socket.accept()
                print(f"[INFO] Accepted connection from {addr}.")
                # Spawn a thread from the pool to handle the connection
                executor.submit(handle_client, conn, addr)


if __name__ == "__main__":
    start_server()
