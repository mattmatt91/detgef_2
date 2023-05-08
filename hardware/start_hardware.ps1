
C:\Labview-Programme\GMA2\GMA_6MFC\Zusatzprogramme\RelayBoard\Programmer\dfu-programmer.exe AT32uc3c2512 launch
cd ..
venv\Scripts\activate
cd hardware
uvicorn main:app --host 127.0.0.1 --port 9010
