

""" this is the TUI element just test and use the backen 
Of this application 


Front end coming sooon

 """


from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from processor import DataProcessingModule, DataCollectionModule
import threading
import sys

class TUI:
    def __init__(self):
        self.console = Console()
        self.data_collector = DataCollectionModule(interface='wlp4s0')
        self.data_processor = DataProcessingModule(self.data_collector)
        self.capture_thread = None
        self.watch_thread = None
        self.stop_event = threading.Event()

    def display_mac_addresses(self):
        """Displays the MAC address of each device on the network."""
        self.console.log("Displaying MAC addresses...")
        self.data_processor.display_mac_addresses()

    def start_packet_capture(self):
        """Start capturing packets."""
        if self.capture_thread and self.capture_thread.is_alive():
            self.console.log("[bold red]Packet capture is already running![/bold red]")
        else:
            self.console.log("Starting packet capture... (Press Enter to stop)")
            self.capture_thread = threading.Thread(target=self._capture_packets)
            self.capture_thread.start()
            self._wait_for_interrupt()

    def _capture_packets(self):
        save_to_file = "netfile/capture.pcap"
        try:
            self.data_processor.data_collector.run(save_to_file=save_to_file)
        except KeyboardInterrupt:
            self.console.log("Packet capture stopped by user.")

    def start_continuous_watch(self):
        """Start the continuous packet watch."""
        if self.watch_thread and self.watch_thread.is_alive():
            self.console.log("[bold red]Continuous watch is already running![/bold red]")
        else:
            self.console.log("Starting continuous watch... (Press Enter to stop)")
            self.watch_thread = threading.Thread(target=self._continuous_watch)
            self.watch_thread.start()
            self._wait_for_interrupt()

    def _continuous_watch(self):
        save_to_file = "netfile/capture.pcap"
        try:
            self.data_processor.continuous_watch(save_to_file=save_to_file)
        except KeyboardInterrupt:
            self.console.log("Continuous watch stopped by user.")

    def _wait_for_interrupt(self):
        """Wait for the user to press Enter to stop the process."""
        try:
            input()
            self.stop_event.set()
            if self.capture_thread and self.capture_thread.is_alive():
                self.console.log("Stopping packet capture...")
                self.capture_thread.join()

            if self.watch_thread and self.watch_thread.is_alive():
                self.console.log("Stopping continuous watch...")
                self.watch_thread.join()
        except KeyboardInterrupt:
            self.console.log("Process interrupted by user.")

    def update_layout(self):
        """Updates the TUI layout."""
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3)
        )

        layout["header"].update(Panel("[bold cyan]Data Processing Module TUI[/bold cyan]"))
        layout["footer"].update(Panel("[bold green]Press 'q' to quit[/bold green]"))

        layout["main"].update(
            Panel(
                "[1] Capture Packets\n"
                "[2] Display MAC Addresses\n"
                "[3] Continuous Watch\n"
                "[q] Quit",
                title="Main Menu"
            )
        )

        self.console.print(layout)

    def stop_threads(self):
        """Stop all running threads."""
        if self.capture_thread and self.capture_thread.is_alive():
            self.console.log("Stopping packet capture...")
            self.stop_event.set()
            self.capture_thread.join()

        if self.watch_thread and self.watch_thread.is_alive():
            self.console.log("Stopping continuous watch...")
            self.stop_event.set()
            self.watch_thread.join()

    def display_menu(self):
        while True:
            self.update_layout()

            choice = self.console.input("[bold yellow]Choose an option: [/bold yellow]").strip()
            self.console.log(f"User selected option: {choice}")

            if choice == '1':
                self.start_packet_capture()
            elif choice == '2':
                self.display_mac_addresses()
            elif choice == '3':
                self.start_continuous_watch()
            elif choice.lower() == 'q':
                self.console.log("Stopping all processes and exiting...")
                self.stop_threads()  # Ensure all threads are stopped
                sys.exit()  # Force the program to exit
            else:
                self.console.log("[bold red]Invalid Option. Please choose again.[/bold red]")

if __name__ == "__main__":
    tui = TUI()
    tui.display_menu()
