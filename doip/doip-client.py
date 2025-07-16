import socket
import struct

class DoIPClient:
    def __init__(self, host, port=13400):
        self.host = host
        self.port = port
        self.sock = None
        
    def connect(self):
        """Establish a TCP connection"""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        
    def disconnect(self):
        """Close the socket connection"""
        if self.sock:
            self.sock.close()
            self.sock = None
            
    def send_diagnostic_message(self, source_addr, target_addr, user_data):
        """Send a diagnostic message to the DoIP server"""
        if not self.sock:
            raise ConnectionError("Not connected")
            
        # DoIP Header
        protocol_version = 0x02
        payload_type = 0x8001  # Diagnostic message
        payload_length = len(user_data) + 4  # 4 bytes for source and target addresses
        
        # Consruct the packet
        header = struct.pack("!BBHL", protocol_version, 0x00, payload_type, payload_length)
        addresses = struct.pack("!HH", source_addr, target_addr)
        
        # Send data
        self.sock.send(header + addresses + user_data)
        
        # Receive response
        response = self.sock.recv(2048)
        return response

def main():
    client = DoIPClient("192.168.1.100")
    try:
        client.connect()
        # Example: Sending a diagnostic message
        response = client.send_diagnostic_message(0x0E00, 0x0E80, b'\x22\xF1\x90')
        print(f"Received response: {response.hex()}")
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()