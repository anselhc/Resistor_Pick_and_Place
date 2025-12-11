import serial
import time


def switch_magnet(string):
    """
    Turns magnet on for h input or off for l input.

    args:
        string - h\n or l\n
    """
    try:
        # Configure the serial port (replace 'COM3' with your port name and 9600 with your baud rate)
        # On Linux, port might be '/dev/ttyAMA0' or '/dev/ttyUSB0'
        # On macOS, it might be something like '/dev/tty.usbmodem...'
        ser = serial.Serial(
            port="/dev/cu.usbmodem101", baudrate=9600, timeout=1
        )

        # Wait a moment for the connection to establish
        time.sleep(2)

        # Data must be sent as bytes. Encode the string to bytes using b'' or .encode()
        data_to_send = b"string"

        # Write the data to the serial port
        ser.write(data_to_send)
        print(f"Sent: {data_to_send.decode().strip()}")

        # Optional: read back any response
        while ser.in_waiting > 0:
            response = ser.readline().decode("utf-8").strip()
            print(f"Received response: {response}")

    except serial.SerialException as e:
        print(f"Error: {e}")

    # Always close the port when done
    # if ser.isOpen():
    #     ser.close()
    #     print("Serial port closed.")
