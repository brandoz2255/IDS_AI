
""" this is the TUI element just test and use the backen 
Of this application 


Front end coming sooon

 """

from rich.console import Console
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from processor import DataProcessingModule, DataCollectionModule


class TUI:
    def __init__(self):
        self.console = Console()
        self.data_collector = DataCollectionModule(interface='wlp4s0')
        self.data_processor = DataProcessingModule(self.data_collector)



    def display_mac_addresses(self):
        """Displays the MAC address of each device on the network."""
        self.console.log("Displaying MAC addresses...")
        self.data_processor.display_mac_addresses()



    def start_packet_capture(self):
        """Start capturing packets."""
        self.console.log("Starting packet capture...")
        save_to_file = "netfile/capture.pcap"
        self.data_processor.data_collector.run(save_to_file=save_to_file)
        self.console.log("Packet capture started.")



    def start_continuous_watch(self):
        """Start the continuous packet watch."""
        self.console.log("Starting continuous watch...")
        save_to_file = "netfile/capture.pcap"
        self.data_processor.continuous_watch(save_to_file=save_to_file)
        self.console.log("Continuous watch started.")



    def display_menu(self):
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )

        layout["header"].update(Panel("[bold cyan]Data Processing Module TUI[/bold cyan]"))
        layout["footer"].update(Panel("[bold green]Press 'q' to quit[/bold green]"))

        with Live(layout, screen=True):
            while True:
                layout["main"].update(
                    Panel(
                        "[1] Capture Packets\n"
                        "[2] Display MAC Addresses\n"
                        "[3] Continuous Watch\n"
                        "[q] Quit",
                        title="Main Menu"
                    )
                )


                choice = self.console.input("[bold yellow]Choose an option: [/bold yellow]").strip()
                self.console.log(f"User selected option: {choice}")
                
                if choice == '1':
                    self.start_packet_capture()
                elif choice == '2':
                    self.display_mac_addresses()
                elif choice == '3':
                    self.start_continuous_watch()
                elif choice.lower() == 'q':
                    self.console.log("Exiting...")
                    break
                else:
                    self.console.log("[bold red]Invalid Option. Please choose again.[/bold red]")



if __name__ == "__main__":
    tui = TUI()
    tui.display_menu()
