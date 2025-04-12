# created by Kevin Trochez Grajeda and Jesus Perez Arias - Team 19
import socket
import threading
import sys
import select

# Global variables to keep track of connections
connections = {}
server_socket = None

# display_help is responsible to only display the menu
# to the user and how the application works
def display_help():
    print("""
Available commands:
1. help                   - Display information about the available commands.
2. myip                   - Display the IP address of this process.
3. myport                 - Display the port this process is listening on.
4. connect <IP> <Port>    - Connect to another peer at the specified IP and port.
5. list                   - Display a numbered list of all active connections.
6. terminate <ID>         - Terminate the connection with the specified ID from the list command.
7. send <ID> <Message>    - Send a message to the peer with the specified ID.
8. exit                   - Close all connections and terminate the program.
    """)


# UDP socket created to get the local
# IP address by connecting to a public google dns server
# as it is the way it will find the local IP.
def get_my_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unable to retrieve IP"

# responsible to receive messages from the parent client socket
def handle_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode() # only 1024 bytes of data is decoded
            if message:
                print(f"Message received from {address[0]}:{address[1]}")
                print(f"Message: \"{message}\"")
            else:
                break
        except:
            break
    print(f"Connection closed with {address[0]}:{address[1]}")
    client_socket.close()
    # go through all connections to remove from the list when disconnect occurs
    for id, (sock, addr) in list(connections.items()):
        if addr == address:
            del connections[id]
            break


# start tcp server and listens to the port
# spawns new thread to handle communication amongst clients
# tracks the global connections
def start_server(port):
    global server_socket # makes global to track other clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")

    while True:
        readable, _, _ = select.select([server_socket], [], [], 0.1)
        for s in readable:
            client_socket, addr = server_socket.accept()
            print(f"New connection from {addr[0]}:{addr[1]}")
            threading.Thread(target=handle_client, args=(client_socket, addr)).start()
            connections[len(connections) + 1] = (client_socket, addr)

# initiate tcp connection to peer (server/client)
# tries to attempt to the peer and tracks the connection dict
# starts thread to handle peer communication
def connect_to_peer(ip, port):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, int(port)))
        print(f"Connected to {ip}:{port}")
        connections[len(connections) + 1] = (client_socket, (ip, int(port)))
        threading.Thread(target=handle_client, args=(client_socket, (ip, int(port)))).start()
    except Exception as e:
        print(f"Connection failed: {e}")


# iterates through connections dict and retrieves socket, id, and address
def list_connections():
    if not connections:
        print("No active connections.")
    else:
        print("Active connections:")
        for id, (sock, addr) in connections.items():
            print(f"{id}: {addr[0]} {addr[1]}")

# closes connection to the connections dict with the matching id and deletes from connection dict
def terminate_connection(conn_id):
    if conn_id in connections:
        client_socket, addr = connections[conn_id]
        client_socket.close()
        del connections[conn_id]
        print(f"Connection with {addr[0]}:{addr[1]} terminated.")
    else:
        print("Invalid connection ID.")

# attempts to send message when matching connection id
def send_message(conn_id, message):
    if conn_id in connections:
        client_socket, _ = connections[conn_id]
        try:
            client_socket.send(message.encode())
            print(f"Message sent to connection {conn_id}")
        except Exception as e:
            print(f"Failed to send message: {e}")
    else:
        print("Invalid connection ID.")


# goes through the menu selection based on the user input and calls the respective method
def command_loop(port):
    threading.Thread(target=start_server, args=(port,), daemon=True).start()

    while True:
        command = input("> ").strip().split()
        if not command:
            continue

        cmd = command[0].lower()
        if cmd == "help":
            display_help()
        elif cmd == "myip":
            print(f"My IP address: {get_my_ip()}")
        elif cmd == "myport":
            print(f"My port: {port}")
        elif cmd == "connect" and len(command) == 3:
            ip, port = command[1], command[2]
            connect_to_peer(ip, int(port))
        elif cmd == "list":
            list_connections()
        elif cmd == "terminate" and len(command) == 2:
            terminate_connection(int(command[1]))
        elif cmd == "send" and len(command) >= 3:
            conn_id = int(command[1])
            message = " ".join(command[2:])
            if len(message) <= 100:
                send_message(conn_id, message)
            else:
                print("Message length exceeds 100 characters.")
        elif cmd == "exit":
            for sock, _ in connections.values():
                sock.close()
            if server_socket:
                server_socket.close()
            print("Exiting the chat application.")
            break
        else:
            print("Invalid command. Type 'help' for a list of commands.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chat.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    command_loop(port)