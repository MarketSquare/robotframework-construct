import serial
import select


_serial_connection = None

def open_nci_connection_via_uart(device: str, baudrate: int):
    """
    Opens a connection to a NCI device via UART.

    Returns a tuple of two file objects, first one for reading and second one for writing.
    """
    global _serial_connection
    _serial_connection = serial.Serial(device, baudrate, timeout=1)
    return (open(_serial_connection.fd, "rb", buffering=0, closefd=False), open(_serial_connection.fd, "wb", buffering=0, closefd=False),)

def close_nci_connection():
    """
    Closes the NCI connection by closing the serial connection.
    """
    global _serial_connection
    if _serial_connection and _serial_connection.is_open:
        _serial_connection.close()
    else:
        raise Exception("NCI connection is not open")

def wait_for_data_from_nci(timeout: float = 1.0):
    """
    Waits for data from the NCI device.

    Uses the select module to wait for data to be available on the serial connection.
    Raises an exception if the NCI connection is not open.
    """
    global _serial_connection
    if _serial_connection and _serial_connection.is_open:
        assert select.select([_serial_connection], [], [], timeout)[0], "Timeout while waiting for data from NCI device"
    else:
        raise Exception("NCI connection is not open")
