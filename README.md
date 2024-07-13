---

# QuicStream: Lightweight QUIC Protocol in Python

This repository contains an implementation of a lightweight version of the QUIC (Quick UDP Internet Connection) protocol in Python. QUIC is a transport protocol developed by Google that aims to improve web performance by reducing latency and enhancing security.

## Features

- **QUIC Client**: Initiates connections to the server, sends requests, and receives responses.
- **QUIC Server**: Listens for incoming connections, processes requests, and sends back responses.
- **Packet Handling**: Defines classes and functions for encoding and decoding QUIC packets, managing sockets, and handling stream payloads.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/WasiimSheb/QuicStream.git
    ```
2. Navigate to the project directory:
    ```bash
    cd QuicStream
    ```

## Usage

Run the server:
```bash
python Server.py
```

Run the client:
```bash
python Client.py
```

## Files and Directories

- **Client.py**: Implementation of the QUIC client.
- **Server.py**: Implementation of the QUIC server.
- **Packets.py**: Classes and functions for packet encoding and decoding.
- **UniTest.py**: Unit tests for the implementation.

## Example

### Running the Server

Start the QUIC server by executing:
```bash
python Server.py
```

### Running the Client

In another terminal, run the QUIC client to connect to the server and send a request:
```bash
python Client.py
```

## Unit Testing

Unit tests are provided to ensure the correctness and reliability of the implementation. Run the tests using:
```bash
python UniTest.py
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Contact

For any inquiries, please contact: anthonisdb@gmail.com, Wasimshebalny@gmail.com, shifaakh28@gmail.com.

---
