Subject to change based on I want it to do!
### 1. **Data Collection Module**

This module will be responsible for gathering network data that needs to be analyzed. Depending on your specific requirements, this could involve capturing live network traffic or processing stored network logs.

- This could do both On how it analyzes network traffic like wireshark
- scans devices connected to a network like NMAP 
- and also like wireshark can processes network logs like nothing
- have it a wireshark/nmap combination 
	- might need to be split up into two modules 

### 2. **Data Processing Module**

After collecting the data, this module will process the raw data into a format suitable for analysis. This might include filtering, data cleaning, and preliminary data transformations.

- Will communicate with Data collection module 

### 3. **Machine Learning Module**

This is a core module where the actual detection logic using machine learning will reside. It will include training models and using them to detect anomalies or malicious activities in the network traffic.

- By providing examples of well bad traffic etc or something need study more on training models 


### 4. **Alert Module**

This module will handle the output from the Machine Learning Module and decide what action to take if malicious activity is detected.

- Decides if there is malicous activity 

### 5. **API Module**

If your system needs to be accessible through web or other services, an API module can serve as an interface for other systems to interact with your IDS.

- This will interact with other modules so that the React front end can use this python app with ease especially the `NMAP` functionality
	- Also figure out ahead of time how can you can dynamically use React to display a map of devices connected to a network Obsidian style
