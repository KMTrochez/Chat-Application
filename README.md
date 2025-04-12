# Python Chat Application
Created by Kevin Trochez Grajeda and Jesus Perez Arias - Team 19

## Features
- View IP Address and port of all connected processes
- Connect to other peers using respective IP address and port
- Managing multiple peer connections
- Send messages to other peers
- Shutdown on all existing connections on program exit

## Prerequisites
Ensure you have python3 installed before running this application.


## How to Run the Application
To run the application run the following bash command in one 
terminal then have another terminal to 
```bash
python chat.py <port>
```

Replace the <port> with the port number you want the application to run on.
```bash
python chat.py 8080
```

### Commands
| Command               | Description                                        |
|-----------------------|----------------------------------------------------|
| `help`                | Display a list of all available commands           |
| `myip`                | Show IP address of machine running  the process    |
| `myport`              | Display the port number the server is listening on |
| `connect <IP> <Port>` | Connect to another peer using their IP and port. Example: `connect 192.168.1.2 9090` |
| `list`                | Show a numbered list of all active connections |
| `terminate <ID>`      | Close the connection with the peer identified by the given ID from the list command. |
| `send <ID> <Message>`  | Send a message to a peer identified by the given ID. Message length must not exceed 100 characters. |
| `exit` | Close all connections and exit the program |

### Example Usage
1. Start the server on the machine via your terminal.
```bash
python chat.py 8080
```

2. On another machine connected to the same network, or another terminal instance, connect to the server.
```bash
python chat.py 8080
```

3. List active connections
```bash
list
```

4. Send a message to a peer
```bash
send 1 Hello, how are you?
```

5. Terminate the connection
```bash
terminate 1
```
## Overview
This chat application allows one client and one receiver to transmit messages
over the true computer IPs and has a global peer connections via 
- The server listens  for incoming connections
- Once connected, the peers can exchange using TCP sockets
- Each peer connection is handled via separate threads
- The `select` module handles multiple connections without blocking the main open thread

### Error Handling
Application attempts to handle common socket errors such as the following:
- Common socket errors
- Failed connections
- Disconnections
- Sending errors via the message command

## License
This project is licensed under the MIT License.
