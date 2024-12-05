import serial
import select


class nci_interface():
    def __init__(self):
        self._serial_connection = None

    def open_nci_connection_via_uart(self, device: str, baudrate: int):
        """
        Opens a connection to a NCI device via UART.

        Returns a tuple of two file objects, first one for reading and second one for writing.
        """
        self._serial_connection = serial.Serial(device, baudrate, timeout=1)
        self._serial_connection.reset_input_buffer()
        return (open(self._serial_connection.fd, "rb", buffering=0, closefd=False), 
                open(self._serial_connection.fd, "wb", buffering=0, closefd=False),)
    
    def wait_for_data_from_nci(self, timeout: float = 1.0):
        """
        Waits for data from the NCI device.
    
        Uses the select module to wait for data to be available on the serial connection.
        Raises an exception if the NCI connection is not open.
        """
        if self._serial_connection and self._serial_connection.is_open:
            assert select.select([self._serial_connection], [], [], timeout)[0], "Timeout while waiting for data from NCI device"
        else:
            raise Exception("NCI connection is not open")

    def close_nci_connection(self):
        """
        Closes the NCI connection by closing the serial connection.
        """
        if self._serial_connection and self._serial_connection.is_open:
            self._serial_connection.close()
        else:
            raise Exception("NCI connection is not open")