

""" this is the TUI element just test and use the backen 
Of this application 


Front end coming sooon

 """


import os
import random
import time
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
        self.console.log("Scanning network for devices...")
        self.data_collector.scan_network("192.168.1.0/24")  # Scan the network first
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
        layout["footer"].update(Panel("[bold green]Press 'q' to quit or 'g' for something special...[/bold green]"))

        layout["main"].update(
            Panel(
                "[1] Capture Packets\n"
                "[2] Display MAC Addresses\n"
                "[3] Continuous Watch\n"
                "[4](g) Does something special....\n"
                "[5](q) Quit",
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



    def snake_game(self):


        """A simple snake game for old times sake...."""


        self.console.clear()
        width, height = 30, 20
        snake = [(width//2, height//2)]
        direction = (0, 1)
        food = (random.randint(0, width-1), random.randint(0, height-1))
        score = 0



        def print_game_board():
            self.console.clear()
            for y in range(height):
                for x in range(width):
                    if (x, y) in snake:
                        print('S', end='')
                    elif (x, y) == food:
                        print('F', end='')
                    else:
                        print('.', end='')
                print()
            print(f'Score: {score}')



        def change_direction(new_direction):
            nonlocal direction
            if new_direction == 'w':
                direction = (0, -1)
            elif new_direction == 's':
                direction = (0, 1)
            elif new_direction == 'a':
                direction = (-1, 0)
            elif new_direction == 'd':
                direction = (1, 0)



        while True:
            print_game_board()
            head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

            if head == food:
                snake.insert(0, head)
                food = (random.randint(0, width-1), random.randint(0, height-1))
                score += 1
            else:
                snake.insert(0, head)
                snake.pop()

            if (head[0] < 0 or head[0] >= width or
                head[1] < 0 or head[1] >= height or
                head in snake[1:]):
                break

            user_input = self.console.input("Press 'w', 'a', 's', 'd' to move: ").strip().lower()
            if user_input in ['w', 'a', 's', 'd']:
                change_direction(user_input)

        self.console.log(f"Game Over! Your final score was {score}. Press Enter to return to the main menu.")
        input()



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
            elif choice == 'g':
                self.snake_game()
            elif choice.lower() == 'q':
                self.console.log("Stopping all processes and exiting...")
                self.stop_threads()  # Ensure all threads are stopped
                sys.exit()  # Force the program to exit
            else:
                self.console.log("[bold red]Invalid Option. Please choose again.[/bold red]")



if __name__ == "__main__":
    tui = TUI()
    tui.display_menu()
