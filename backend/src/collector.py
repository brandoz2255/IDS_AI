import scapy.all as scapy
import socket
import threading
import netifaces


"""
GOAL IS TO DO THIS -->

### 1. **Data Collection Module**

This module will be responsible for gathering network data that needs to be analyzed. Depending on your specific requirements, this could involve capturing live network traffic or processing stored network logs.

- This could do both On how it analyzes network traffic like wireshark
- scans devices connected to a network like NMAP 
- and also like wireshark can processes network logs like nothing
- have it a wireshark/nmap combination 
	- might need to be split up into two modules 

  """

class DataCollectionModule:

    def __init__(self, interface='wlp4s0'):
        self.interface = interface
        self.devices = []


    def list_interfaces(self):
        """WILL LIST ALL AVAILABLE NETWORK INTERFACES"""
        interfaces = netifaces.interfaces()
        print("Available network interfaces:")
        for iface in interfaces:
            print(iface)


    def capture_packets(self, packet_count=10):
        """Capture live network traffic."""
        print(f"Capturing {packet_count} packets on {self.interface}...")
        packets = scapy.sniff(iface=self.interface, count=packet_count)
        for packet in packets:
            print(packet.summary())


    def scan_network(self, ip_range):
        """Scan devices connected to a network."""
        print(f"Scanning devices in the network range: {ip_range}")
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast/arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

        
        devices = []
        for element in answered_list:
            device_info = {'ip': element[1].psrc, 'mac': element[1].hwsrc}
            devices.append(device_info)
            print(f"IP: {device_info['ip']}, MAC: {device_info['mac']}")
        self.devices = devices


    def process_logs(self, log_file):
        """Process network logs."""
        print(f"Processing log file: {log_file}")
        with open(log_file, 'r') as file:
            logs = file.readlines()
            for log in logs:
                print(log.strip())


    def run(self):
        """Run the data collection module."""
        capture_thread = threading.Thread(target=self.capture_packets)
        capture_thread.start()


        scan_thread = threading.Thread(target=self.scan_network, args=("192.168.1.0/24",))
        scan_thread.start()


        capture_thread.join()
        scan_thread.join()

if __name__ == "__main__":
    data_collector = DataCollectionModule(interface='wlp4s0')
    data_collector.list_interfaces()
    
    

    # Now, run the data collection tasks
    data_collector.run()