from __future__ import annotations

from src.hex_address import HexAddress


class BinaryDump:
    def __init__(self, content):
        '''
        Initializes a BinaryDump object with the provided content.

        Parameters:
        - content: Initial content for the BinaryDump.
        '''
        self._array = bytearray(content)
        self._size = len(content)

    def get_part(self, address: HexAddress, size: int):
        '''
        Retrieves a part of the BinaryDump starting from the specified address.

        Parameters:
        - address (HexAddress): Starting address for the part.
        - size (int): Size of the part to retrieve.

        Returns:
        - BinaryDump: A new BinaryDump containing the specified part.
        '''
        assert isinstance(address, HexAddress)
        assert isinstance(size, int)
        adr = address.to_int()
        return BinaryDump(self._array[adr:adr + size])

    def hex(self):
        '''
        Returns the hexadecimal representation of the BinaryDump content.

        Returns:
        - str: Hexadecimal representation.
        '''
        return self._array.hex().upper()

    def __str__(self):
        '''
        Returns the hexadecimal representation when the object is converted to a string.

        Returns:
        - str: Hexadecimal representation.
        '''
        return self.hex()

    def add_file_to_address(self, address: HexAddress, code_file: BinaryDump):
        '''
        Adds the content of another BinaryDump to the specified address.

        Parameters:
        - address (HexAddress): Address where the content will be added.
        - code_file (BinaryDump): BinaryDump containing the content to add.
        '''
        assert isinstance(address, HexAddress)
        self.write_bytes(address, bytes(code_file._array))
        pass

    def write_long(self, address: HexAddress, value: int):
        '''
        Writes a 4-byte (long) integer value to the specified address.

        Parameters:
        - address (HexAddress): Address where the value will be written.
        - value (int): Value to write.
        '''
        assert isinstance(address, HexAddress)
        assert isinstance(value, int)
        self._write_value(address, value, 4)

    def write_short(self, address: HexAddress, value: int):
        '''
        Writes a 2-byte (short) integer value to the specified address.

        Parameters:
        - address (HexAddress): Address where the value will be written.
        - value (int): Value to write.
        '''
        assert isinstance(address, HexAddress)
        assert isinstance(value, int)
        self._write_value(address, value, 2)

    def write_byte(self, address: HexAddress, value: int):
        '''
        Writes a 1-byte (byte) integer value to the specified address.

        Parameters:
        - address (HexAddress): Address where the value will be written.
        - value (int): Value to write.
        '''
        assert isinstance(address, HexAddress)
        assert isinstance(value, int)
        self._write_value(address, value, 1)

    def _write_value(self, address: HexAddress, value: int, bytes_count: int):
        '''
        Writes an integer value to the specified address with the specified byte count.

        Parameters:
        - address (HexAddress): Address where the value will be written.
        - value (int): Value to write.
        - bytes_count (int): Number of bytes representing the value.
        '''
        assert isinstance(address, HexAddress)
        assert isinstance(value, int)
        assert isinstance(bytes_count, int)
        value_bytes = value.to_bytes(bytes_count, 'big')
        self.write_bytes(address, value_bytes)

    def write_bytes(self, address2: HexAddress, value_bytes: bytes):
        '''
        Write a sequence of bytes to the specified address.

        Parameters:
        - address2 (HexAddress): The address where the bytes will be written.
        - value_bytes (bytes): The bytes to be written.
        '''
        assert isinstance(address2, HexAddress)
        assert isinstance(value_bytes, bytes)

        address = address2.to_int()

        # Check if the address is within the bounds of the content
        if address < 0 or address >= len(self._array):
            raise ValueError("Address is out of bounds")

        # Calculate the end address based on the value length
        end_address = address + len(value_bytes)

        # Check if the end address is within the bounds of the content
        if end_address > len(self._array):
            raise ValueError("Value exceeds the length of the content")

        self._array = self._array[:address] + value_bytes + self._array[address + len(value_bytes):]

    def get_bytes(self):
        return self._array
