import scapy.all as scapy
import threading
import os
from collector import DataCollectionModule
import time



""" 

### 2. **Data Processing Module**

After collecting the data, this module will process the raw data into a format suitable for analysis. This might include filtering, data cleaning, and preliminary data transformations.

- Will communicate with Data collection module 
- Read the data and include filtering 
- Will include Data Cleaning feature 
- will include Data transformations 
- Will include displaying the mac addresses of each device on the network 
- Continuously watch the data live


 """

class DataProcessingModule:
    def __init__(self, data_collector):
        self.data_collector = data_collector
        self.filtered_packets = []
        self.clean_packets = []



    def read_pcap(self, pcap_file):
        """Read the captured packets from a pcap file."""
        print(f"Reading packets from {pcap_file}...")
        return scapy.rdpcap(pcap_file)
    


    def filter_packets(self, packets, filter_condition):
        """Filter packets based on a specific condition."""
        print("Filtering packets...")
        self.filtered_packets = [packet for packet in packets if filter_condition(packet)]
        print(f"{len(self.filtered_packets)} packets after filtering.")



    def clean_data(self):
        """Perform data cleaning on the filtered packets."""
        print("Cleaning data...")
        self.clean_packets = [packet for packet in self.filtered_packets if self.is_valid_packet(packet)]
        print(f"{len(self.clean_packets)} packets after cleaning.")



    def is_valid_packet(self, packet):
        """Check if a packet is valid. This is a placeholder for actual validation logic."""
        # Example validation: Check if the packet has an IP layer
        return packet.haslayer(scapy.IP)



    def transform_data(self):
        """Transform data as needed for analysis."""
        print("Transforming data...")
        # Placeholder for transformation logic
        transformed_data = []
        for packet in self.clean_packets:
            transformed_data.append({
                "src_ip": packet[scapy.IP].src,
                "dst_ip": packet[scapy.IP].dst,
                "protocol": packet[scapy.IP].proto,
                "length": len(packet)
            })
        print("Data transformation complete.")
        return transformed_data



    def display_mac_addresses(self):
        """Display the MAC addresses of each device on the network."""
        print("Displaying MAC addresses...")
        for device in self.data_collector.devices:
            print(f"Device IP: {device['ip']}, MAC Address: {device['mac']}")



    def continuous_watch(self, save_to_file=None):
        """Continuously watch live data and process it."""
        print("Starting continuous data watch...")
        capture_thread = threading.Thread(target=self.data_collector.capture_packets_continuous, kwargs={'save_to_file': save_to_file})
        capture_thread.start()

        last_packet_count = 0

        while capture_thread.is_alive():
            time.sleep(2)  # Add a delay to prevent constant file reading
            if save_to_file and os.path.exists(save_to_file):
                packets = self.read_pcap(save_to_file)
                
                if len(packets) > last_packet_count:
                    new_packets = packets[last_packet_count:]  # Process only new packets
                    last_packet_count = len(packets)
                    
                    self.filter_packets(new_packets, lambda pkt: pkt.haslayer(scapy.IP))  # Example filter condition
                    self.clean_data()
                    transformed_data = self.transform_data()
                    print(transformed_data)
                else:
                    print("No new packets to process.")

        capture_thread.join()
        print("Continuous watch ended.")




class DataCollectionModule:
    def __init__(self, interface='wlp4s0'):
        self.interface = interface
        self.devices = []



    def list_interfaces(self):
        """ WILL LIST ALL AVAILABLE NETWORK INTERFACES """
        interfaces = netifaces.interfaces()
        print("Available network interfaces:")
        for iface in interfaces:
            print(iface)



    def capture_packets_continuous(self, save_to_file=None):
        """Continuously capture live network traffic and save to a file."""
        print(f"Capturing packets on {self.interface} continuously...")
        try:
            while True:
                packets = scapy.sniff(iface=self.interface, count=10)
                
                if save_to_file:
                    scapy.wrpcap(save_to_file, packets, append=True)
                    print(f"Captured packets appended to {save_to_file}")

                for packet in packets:
                    print(packet.summary())
                
                time.sleep(1)  # Add a short delay between captures

        except KeyboardInterrupt:
            print("Stopping continuous capture.")



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



    def run(self, pcap_file=None, save_to_file=None):
        """Runs the data collection module."""
        if pcap_file:
            print("Scanning captured traffic...")
            self.scan_captured_traffic(pcap_file)
        else:
            capture_thread = threading.Thread(target=self.capture_packets_continuous, kwargs={'save_to_file': save_to_file})
            capture_thread.start()

            scan_thread = threading.Thread(target=self.scan_network, args=("192.168.1.0/24",))
            scan_thread.start()

            capture_thread.join()
            scan_thread.join()




if __name__ == "__main__":
    data_collector = DataCollectionModule(interface='wlp4s0')
    data_processor = DataProcessingModule(data_collector)

    save_to_file = "netfile/capture.pcap"
    data_processor.data_collector.run(save_to_file=save_to_file)

    data_processor.display_mac_addresses()
    data_processor.continuous_watch(save_to_file=save_to_file)
