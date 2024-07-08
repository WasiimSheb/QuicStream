import random
import socket
import struct
import pickle
import sys

LONG_HEADER_FLAG = 1
SHORT_HEADER_FLAG = 0

def generate_random_hex():
    # Generate a random integer between 0 and (2^64 - 1)
    random_int = random.randint(0, 2**64 - 1)
    # Convert the integer to hexadecimal and remove the '0x' prefix
    hex_string = hex(random_int)[2:]
    # Ensure the hex string is 16 characters long (8 bytes)
    hex_string = hex_string.zfill(16)
    return hex_string

class QUICPacket:
    def __init__(self, flags, dest_conn_id, packet_number, protected_payload: list):
        self.flags = flags
        self.dest_conn_id = dest_conn_id
        self.packet_number = packet_number
        self.protected_payload = protected_payload

    def encode(self):
        return pickle.dumps(self)
    
    @classmethod
    def decode(cls, data):
        return pickle.loads(data)

    def __str__(self):
        str = f"Flags: {self.flags} Dest Conn ID: {self.dest_conn_id} Packet Number: {self.packet_number}"
        str +=  "Payload: " 
        for payload in self.protected_payload:
            str += f"{payload.__str__()}"
        str += "\n"
        return str
    
    def size_in_bytes(self):
        flags_size = sys.getsizeof(self.flags)
        dest_conn_id_size = sys.getsizeof(self.dest_conn_id)
        packet_number_size = sys.getsizeof(self.packet_number)
        payload_size = sys.getsizeof(self.protected_payload)

        total_size = flags_size + dest_conn_id_size + packet_number_size + payload_size
        return total_size



class QUICStreamPayload:
    def __init__(self, stream_id, offset, length, finished, stream_data):
        self.stream_id = stream_id
        self.offset = offset
        self.finished = finished
        self.length = length
        self.stream_data = stream_data

    def encode(self):
        return pickle.dumps(self)

    @classmethod
    def decode(cls, data):
        return pickle.loads(data) 
    
    def __str__(self):
        return f"Stream ID: {self.stream_id} Offset: {self.offset} Finished: {self.finished} Length: {self.length} "

class QUICLongHeader:
    def __init__(self, flags ,dest_conn_id, src_conn_id, packet_number):
        self.flags = flags
        self.dest_cid = dest_conn_id
        self.src_cid = src_conn_id
        self.packet_number = packet_number

    def encode(self):
        return pickle.dumps(self)  

    @classmethod
    def decode(cls, data):
        return pickle.loads(data)
    

class QUICSocket:
    def __init__(self):
        self.__address = None
        self.__dest_cid = None
        self.__src_cid = None
        self.__sockfd = None

    def create_socket(self):
        self.__sockfd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if self.__sockfd is None:
            raise RuntimeError("Socket creation failed.")
        self.__sockfd.settimeout(3)
        self.__sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sockfd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)

    def bind(self, address):
        if self.__sockfd:
            self.__sockfd.bind(address)

    def close(self):
        if self.__sockfd:
            self.__sockfd.close()

    def sendto(self, data, address):
        if not self.__sockfd:
            raise RuntimeError("Socket not initialized. Call create_socket() first.")
        try:
            self.__sockfd.sendto(data, address)
        except (KeyboardInterrupt, socket.timeout) as e:
            print(e)
            print("Exiting...")
            self.__sockfd.close()
            exit(0)

    def recvfrom(self, bufsize):
        if not self.__sockfd:
            raise RuntimeError("Socket not initialized. Call create_socket() first.")
        try:
            return self.__sockfd.recvfrom(bufsize)
        except (KeyboardInterrupt, socket.timeout) as e:
            print(e)
            print("Exiting...")
            self.__sockfd.close()
            exit(0)
    
    # Setters
    def set_address(self, address):
        self.__address = address
    
    def set_dest_cid(self, dest_cid):
        self.__dest_cid = dest_cid
    
    def set_src_cid(self, src_cid):
        self.__src_cid = src_cid
    
    # Getters
    def get_address(self):
        return self.__address
    
    def get_dest_cid(self):
        return self.__dest_cid
    
    def get_src_cid(self):
        return self.__src_cid
    
    def get_sockfd(self):
        if not self.__sockfd:
            raise RuntimeError("Socket not initialized. Call create_socket() first.")
        return self.__sockfd

class QUICAck:
    def __init__(self, ack_number, ack_delay):
        self.ack_number = ack_number
        self.ack_delay = ack_delay

    def encode(self):
        try:
            return pickle.dumps(self)
        except pickle.PickleError as e:
            print(f"Error encoding QUICPacket: {e}")
            return None

    @classmethod
    def decode(cls, data):
        try:
            return pickle.loads(data)
        except pickle.UnpicklingError as e:
            print(f"Error decoding QUICPacket: {e}")
            return None
