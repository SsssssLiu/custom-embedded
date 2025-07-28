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
        """
        Send a diagnostic message to the DoIP server
        Returns: List of responses [doip_ack, uds_response]. doip_ack may be None for single-response messages
        """
        if not self.sock:
            raise ConnectionError("Not connected")
            
        # DoIP Header
        protocol_version = 0x02
        payload_type = 0x8001  # Diagnostic message
        payload_length = len(user_data) + 4  # 4 bytes for source and target addresses
        
        # Construct the packet
        header = struct.pack("!BBHL", protocol_version, 0x00, payload_type, payload_length)
        addresses = struct.pack("!HH", source_addr, target_addr)
        
        # Send data
        self.sock.send(header + addresses + user_data)
        
        # Try to receive DoIP ACK first (non-blocking)
        self.sock.setblocking(False)
        try:
            ack = self.sock.recv(8)  # DoIP header is 8 bytes
            if len(ack) >= 8:
                ack_type = struct.unpack("!L", ack[4:8])[0]
                if ack_type != 0x8002:  # Not a DoIP ACK
                    ack = None
        except socket.error:
            ack = None
    
        # Switch back to blocking mode for UDS response
        self.sock.setblocking(True)
        response = self.sock.recv(2048)
        
        return [ack, response]

    def send_file(self, des_ip: str, file_path: str) -> bool:
        """
        Send a file using UDS services sequence:
        1. DiagnosticSessionControl (0x10) to switch to programming session
        2. SecurityAccess (0x27) for authentication
        3. RequestDownload (0x34) to initiate transfer
        4. TransferData (0x36) to send file chunks
        5. TransferExit (0x37) to complete transfer
        """
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                file_data = f.read()
                file_size = len(file_data)

            # Step 1: Switch to programming session
            responses = self.send_diagnostic_message(0x0E00, 0x0E80, b'\x10\x02')
            if responses[1][12] != 0x50:  # Check UDS response
                raise Exception("Failed to enter programming session")

            # Step 2: Security Access
            responses = self.send_diagnostic_message(0x0E00, 0x0E80, b'\x27\x01')
            if responses[1][12] != 0x67:
                raise Exception("Security access denied")

            # Step 3: Request Download
            # Format: 0x34 + Data Format ID + Address and Length Format ID + Memory Address + Memory Size
            req_download = self.send_diagnostic_message(0x0E00, 0x0E80, 
                b'\x34\x00\x44' + file_size.to_bytes(4, 'big'))
            if req_download[0] != 0x74:  # Positive response
                raise Exception("Download request failed")

            # Get max block size from response (assuming it's in the last 2 bytes)
            block_size = min(0x800, int.from_bytes(req_download[-2:], 'big'))

            # Step 4: Transfer Data in chunks
            block_counter = 1
            for i in range(0, file_size, block_size):
                chunk = file_data[i:i + block_size]
                transfer_msg = b'\x36' + block_counter.to_bytes(1, 'big') + chunk
                response = self.send_diagnostic_message(0x0E00, 0x0E80, transfer_msg)
                
                if response[0] != 0x76:  # Positive response
                    raise Exception(f"Transfer failed at block {block_counter}")
                
                block_counter = (block_counter + 1) % 0xFF

            # Step 5: Transfer Exit
            exit_msg = self.send_diagnostic_message(0x0E00, 0x0E80, b'\x37')
            if exit_msg[0] != 0x77:  # Positive response
                raise Exception("Transfer exit failed")

            return True

        except Exception as e:
            print(f"File transfer failed: {str(e)}")
            return False

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