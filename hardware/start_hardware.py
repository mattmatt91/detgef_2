import uvicorn
import signal
import sys

def handle_shutdown(signal, frame):
    # Perform cleanup actions here
    print("Shutting down...")
    sys.exit(0)

if __name__ == "__main__":
    # Register the signal handler
    signal.signal(signal.SIGINT, handle_shutdown)

    try:
        # Start the FastAPI app using uvicorn
        uvicorn.run("main:app", host="127.0.0.1", port=9010)
    except KeyboardInterrupt:
        # Handle keyboard interrupt
        handle_shutdown(signal.SIGINT, None)