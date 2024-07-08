import socket
import sys
from typing import Final
import Packets 
import os
import random
import math

portNumber:Final = 8888
oneMB:Final = 1024 * 1024
fiveMB:Final = 5 * oneMB
minNumberOfBytes:Final = 1000
maxNumberOfBytes:Final = 2000

class QUICServer:
    def __init__(self, host='127.0.0.1', port=portNumber):
        self.host = host
        self.port = port
        self.socket = Packets.QUICSocket()
        self.streams = []  # List to store active streams
        self.i=0

    def create_socket(self):
        print("Creating socket...\n")
        self.socket.create_socket()
        self.socket.bind((self.host, self.port))

    def accept(self):
        
        self.create_socket()
        print("Accepting connection...\n")
        data, address = self.socket.recvfrom(1024)  
        self.socket.set_address(address)
        data = Packets.QUICLongHeader.decode(data)
        self.socket.set_src_cid(data.dest_cid)
        dest_conn_id = Packets.generate_random_hex()
        self.socket.set_dest_cid(dest_conn_id)
        print(f"Received Client Hello from {address}")
        qlh = Packets.QUICLongHeader(Packets.LONG_HEADER_FLAG, dest_conn_id, data.dest_cid, data.packet_number)
        self.socket.sendto(qlh.encode(), address)

        print(f"Sent Server Hello to {address}")

    def send_packet(self, packet, address):
        self.socket.sendto(packet.encode(), address)

    def receive_packet(self):
        data, _ = self.socket.recvfrom(1024) # Adjust buffer size accordingly
        decoded_header = Packets.QUICPacket.decode(data)
        if not isinstance(decoded_header, Packets.QUICPacket):
            print("Invalid packet received. Exiting...")
            self.socket.close()
            exit(1)
        return decoded_header
    
    def receive_ack(self):
        data, _ = self.socket.recvfrom(1024)
        decoded_header = Packets.QUICAck.decode(data)
        if not isinstance(decoded_header, Packets.QUICAck):
            print("Invalid ACK packet received. Exiting...")
            self.socket.close()
            exit(1)
        return decoded_header


    def handle_client(self):
        (self.socket.get_sockfd()).settimeout(None)
        packet = self.receive_packet()
        (self.socket.get_sockfd()).settimeout(3)
        # Check if stream exists
        if(packet.flags == 0):
            for frame in packet.protected_payload:
                if frame.stream_id not in self.streams:
                    self.streams.append({'id': frame.stream_id, 'data': b'', 'totalSent': 0})
        
        # generates streams and sends data
        streamNumber= len(packet.protected_payload)
        print(f"Recieved request for {streamNumber} streams\n")
        self.generate_random_data(streamNumber)
        self.send_data(streamNumber)
    
    # this function genrates random data for the stream
    def generate_random_data(self, stream_number):
        for i in range(stream_number):
            data = os.urandom(random.randint(oneMB, fiveMB)) # Generate 1 MB - 5 MB of random data
            self.streams[i]['data'] = data
        

    # function that divides the data into chunks and sends its via stream
    def send_data(self,streamNumber):
        print("Sending files...\n")
        for i in range(streamNumber):
            r = random.randint(minNumberOfBytes,maxNumberOfBytes) # Generate random chunk size between 1000 and 2000 bytes
            self.streams[i]['chunkSize'] = r
            
        max_packets = -sys.maxsize - 1
        for stream in self.streams:
            max = math.ceil(len(stream['data']) / stream['chunkSize'])
            if max > max_packets:
                max_packets = max
            
        # divide the data into chunks and send it via stream
        for i in range(max_packets):
            frames=[]
            for j in range(streamNumber):
                offset = self.streams[j]['chunkSize'] * i
                
                if offset + self.streams[j]['chunkSize'] >= len(self.streams[j]['data']):
                    remaining = len(self.streams[j]['data']) - offset
                else : 
                    remaining = self.streams[j]['chunkSize']

                data = self.streams[j]['data'][offset:offset + remaining]
                self.streams[j]['totalSent'] += len(data)
                totalSent = self.streams[j]['totalSent']
                if offset + remaining >= len(self.streams[j]['data']):
                    finished = 1
                else:
                    finished = 0
                streamPayload = Packets.QUICStreamPayload(stream_id=j, offset=totalSent, finished=finished, length=len(data), stream_data=data)
                frames.append(streamPayload)
            packet = Packets.QUICPacket(0, self.socket.get_dest_cid(), i, frames)
            
            self.send_packet(packet, self.socket.get_address())

            # Receive ACK
            self.receive_ack()
            
        print("Files sent.\n")


if __name__ == "__main__":
    print("Server Running")
    server = QUICServer()
    server.accept()
    server.handle_client()
    server.socket.close()