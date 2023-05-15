import pyvisa as visa
rm = visa.ResourceManager()
rm.list_resources()

print(rm.list_resources())
