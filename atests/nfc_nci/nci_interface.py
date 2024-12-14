import serial
import select
import time


class nci_interface():
    def __init__(self):
        self._serial_connection = None

    def open_nci_connection_via_uart(self, device: str, baudrate: int, timeout=1.0):
        """
        Opens a connection to a NCI device via UART.

        Returns a tuple of two file objects, first one for reading and second one for writing.
        """
        class timeoutExceptionOnTimeoutSerial(serial.Serial):
            def read(self, size=1):
                retBuf = super().read(size)
                assert len(retBuf) >= size, f"Timeout while reading from serial port, received {len(retBuf)} bytes instead of {size}"
                assert len(retBuf) == size, f"Received more data ({len(retBuf)}) then requested ({size}). "
                return retBuf

        self._serial_connection = timeoutExceptionOnTimeoutSerial(device, baudrate, timeout=timeout)
        self._serial_connection.reset_input_buffer()
        return self._serial_connection # Alternatively, on linux we can use self._serial_connection.fileno() + select instead of the timeout read...


    def wait_for_data_from_nci(self, timeout: float = 1.0):
        """
        Waits for data from the NCI device.

        Raises an exception if the NCI connection is not open.
        """
        if self._serial_connection and self._serial_connection.is_open:
            try:
                select.select([self._serial_connection.fileno()], [], [], timeout)
            except AttributeError:
                    # Windows does not support select on serial ports, so we have to do it the hard way
                    endTime = time.time() + timeout
                    while time.time() < endTime and not self._serial_connection.in_waiting:
                        time.sleep(0.001)
                    assert self._serial_connection.in_waiting, "Timeout while waiting for data from NCI device"
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

    def nci_connection_receive_buffer_should_be_empty(self):
        assert 0 == self._serial_connection.in_waiting

    def empty_nci_connection_receive_buffer(self):
        while self._serial_connection.in_waiting:
            self._serial_connection.read(self._serial_connection.in_waiting)
