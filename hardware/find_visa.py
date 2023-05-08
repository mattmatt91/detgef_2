import pyvisa
from time import sleep




# Initialize the visa library
rm = pyvisa.ResourceManager()

# List all connected devices
devices = rm.list_resources()

# Print the list of devices
print(devices)