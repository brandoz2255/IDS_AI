import scapy.all as scapy
import socket
import threading
import netifaces
import os


"""
GOAL IS TO DO THIS -->

### 1. **Data Collection Module**

This module will be responsible for gathering network data that needs to be analyzed. Depending on your specific requirements, this could involve capturing live network traffic or processing stored network logs.

- This could do both On how it analyzes network traffic like wireshark
- scans devices connected to a network like NMAP 
- and also like wireshark can processes network logs like nothing
- have it a wireshark/nmap combination 
	- might need to be split up into two modules 


             (
                .            )        )
                         (  (|              .
                     )   )\/ ( ( (
             *  (   ((  /     ))\))  (  )    )
           (     \   )\(          |  ))( )  (|
           >)     ))/   |          )/  \((  ) 
           (     (      .        -.     V )/   )(    (
            \   /     .   \            .       \))   ))
              )(      (  | |   )            .    (  /
             )(    ,'))     \ /          \( `.    )
             (\>  ,'/__      ))            __`.  /
            ( \   | /  ___   ( \/     ___   \ | ( (
             \.)  |/  /   \__      __/   \   \|  ))
            .  \. |>  \      | __ |      /   <|  /
                 )/    \____/ :..: \____/     \ <
          )   \ (|__  .      / ;: \          __| )  (
         ((    )\)  ~--_     --  --      _--~    /  ))
          \    (    |  ||               ||  |   (  /
                \.  |  ||_             _||  |  /
                  > :  |  ~V+-I_I_I-+V~  |  : (.
                 (  \:  T\   _     _   /T  : ./
                  \  :    T^T T-+-T T^T    ;<
                   \..`_       -+-       _'  )
         )            . `--=.._____..=--'. ./

  """



class DataCollectionModule:
    def __init__(self, interface='wlp4s0'):
        self.interface = interface
        self.devices = []


    def list_interfaces(self):
        """ WILL LIST ALL AVAILBLE NETWORK INTERFACES """


        interfaces = netifaces.interfaces()
        print("Available network interfaces:")
        for iface in interfaces:
            print(iface)




    def capture_packets(self, packet_count=20, save_to_file=None):
        """Capture live network traffic."""


        print(f"Capturing {packet_count} packets on {self.interface}...")
        packets = scapy.sniff(iface=self.interface, count=packet_count)
        

        if save_to_file:


            save_dir = os.path.dirname(save_to_file)

            
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir)
                print(f"Directory {save_dir} created.")


            scapy.wrpcap(save_to_file, packets)
            print(f"Captured packets saved to {save_to_file}")
        

        for packet in packets:
            print(packet.summary())

        """ wrpcap is responsible for saving pcap files from my network """


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


    def scan_captured_traffic(self, pcap_file):
        """ Scans already captured network traffic """


        print(f"Scanning Packets from {pcap_file} ......")
        packets = scapy.rdpcap(pcap_file)
        for packet in packets:
            print(packet.summary())


    def run(self, pcap_file=None, save_to_file=None):
        """Runs the data collection module. BEEP BOOP BOP!"""


        if pcap_file:
            self.scan_captured_traffic(pcap_file)

        else:
            capture_thread = threading.Thread(target=self.capture_packets, kwargs={'save_to_file': save_to_file})
            capture_thread.start()


            scan_thread = threading.Thread(target=self.scan_network, args=("192.168.1.0/24",))
            scan_thread.start()

            capture_thread.join()
            scan_thread.join()

        
""" main Function duhh sillies !  """


if __name__ == "__main__":
    data_collector = DataCollectionModule(interface='wlp4s0')
    data_collector.list_interfaces()

    # Added options: capture live traffic, save to a file, or analyze a pcap file
    pcap_file = input("-->  |Enter path to pcap file to analyze (or leave empty to capture live traffic): ").strip()
    if pcap_file:
        data_collector.run(pcap_file=pcap_file)
    else:
        print("-----------------------------------------------------------------------------------------------------------------------------")
        save_to_file = input("-->  |Enter path to save captured packets (or leave empty to not save): ").strip()
        data_collector.run(save_to_file=save_to_file)