from src.binarydump import BinaryDump
from src.dump_file import read_dump_file
from src.hex_address import HexAddress


def find_pattern_address(dump: BinaryDump, hex_pattern: str) -> HexAddress:
    search_pattern = bytes.fromhex(hex_pattern)
    index = dump.get_bytes().find(search_pattern)
    if index == -1:
        raise Exception('Pattern not found: ' + hex_pattern)
    return HexAddress(index)


def pick_null_terminated_string(dump: BinaryDump):
    '''
    Picks a null-terminated string from the binary dump.

    Parameters:
    - dump (binarydump.BinaryDump): The binary dump to extract the null-terminated string from.

    Returns:
    - str: The extracted null-terminated string.
    '''
    bin = dump.get_bytes()
    index_of_zero = bin.find(b'\x00')
    if index_of_zero != -1:
        bin = bin[:index_of_zero]
    else:
        raise Exception('Zero not found!')
    result_string = bin.decode("ascii")

    return result_string


class EcuIdentNotPossibleException(Exception):
    pass


class EcuId:
    def __init__(self, bosch_hw_number, bosch_sw_number, bosch_sw_version, vag_part_number, vag_sw_version,
                 vag_engine_info):
        self.bosch_hw_number = bosch_hw_number
        self.bosch_sw_number = bosch_sw_number
        self.bosch_sw_version = bosch_sw_version
        self.vag_part_number = vag_part_number
        self.vag_sw_version = vag_sw_version
        self.vag_engine_info = vag_engine_info

    def __str__(self):
        return f"Bosch Hardware Number : {self.bosch_hw_number}\n" \
               f"Bosch Software Number : {self.bosch_sw_number}\n" \
               f"Bosch Software Version: {self.bosch_sw_version}\n" \
               f"VAG Part Number       : {self.vag_part_number}\n" \
               f"VAG Software Version  : {self.vag_sw_version}\n" \
               f"VAG Engine Info       : {self.vag_engine_info}"


def read_ecu_id(dump: BinaryDump) -> EcuId:
    signature_map = (
        "9B06000C",
        "9B06000F",
        "9A060004",
        "9206000A",
        "9406000A",
        "87060007",
    )
    SGIDB = {}
    i = 0
    for signature in signature_map:
        try:
            signature_address = find_pattern_address(dump, signature)
        except Exception:
            raise EcuIdentNotPossibleException("ECU Ident not possible. Is it a MED9-Binary?")
        signature_address = signature_address + 4
        sgi_db_address = dump.get_part(signature_address, 4)
        sgi_db_address = HexAddress(int.from_bytes(sgi_db_address.get_bytes(), byteorder='big'))
        sgi_db_address = sgi_db_address - 0x400000
        id = pick_null_terminated_string(dump.get_part(sgi_db_address, 40))
        id = id.strip()
        i = i + 1
        SGIDB[i] = id

    return EcuId(
        SGIDB[4],
        SGIDB[5],
        SGIDB[6],
        SGIDB[1],
        SGIDB[3],
        SGIDB[2]
    )


if __name__ == '__main__':
    # Create a Compiler instance with the JSON file path
    file = read_dump_file("test.bin")
    print(read_ecu_id(file))
