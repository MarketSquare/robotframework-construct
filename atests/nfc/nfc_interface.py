import serial
import select
import io
import time


class nfc_interface():
    def __init__(self):
        self._serial_connection = None

    def open_nfc_connection_via_uart(self, device: str, baudrate: int, timeout=1.0):
        """
        Opens a connection to a NFC device via UART.

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


    def wait_for_data_from_nfc(self, timeout: float = 1.0):
        """
        Waits for data from the NFC device.

        Raises an exception if the NFC connection is not open.
        """
        if self._serial_connection and self._serial_connection.is_open:
            try:
                select.select([self._serial_connection.fileno()], [], [], timeout)
            except io.UnsupportedOperation:
                    # Windows does not support select on serial ports, so we have to do it the hard way
                    endTime = time.time() + timeout
                    while time.time() < endTime and not self._serial_connection.in_waiting:
                        time.sleep(0.001)
            assert self._serial_connection.in_waiting, "Timeout while waiting for data from NFC device"
        else:
            raise Exception("NFC connection is not open")

    def close_nfc_connection(self):
        """
        Closes the NFC connection by closing the serial connection.
        """
        if self._serial_connection and self._serial_connection.is_open:
            self._serial_connection.close()
        else:
            raise Exception("NFC connection is not open")

    def nfc_connection_receive_buffer_should_be_empty(self):
        """
        Verifies that the receive buffer is empty.
        """
        assert 0 == self._serial_connection.in_waiting

    def empty_nfc_connection_receive_buffer(self):
        """
        Empties the receive buffer.

        (This is necessary because the HW reset has not been implemented)
        """
        while self._serial_connection.in_waiting:
            self._serial_connection.read(self._serial_connection.in_waiting)
