from typing import List

from src.binarydump import BinaryDump
from src.dump_file import read_dump_file
from src.hex_address import HexAddress


class Variable:
    def __init__(self, name: str, file_address: HexAddress, value: HexAddress, register: str):
        self.name = name
        self.file_address = file_address
        self.value = value
        self.register = register


class ExposedVariable:
    def __init__(self, name: str, file_address: HexAddress):
        self.name = name
        self.file_address = file_address


class InsertPayloadCommand:

    def __init__(self, address: HexAddress, file: BinaryDump, variables: List[Variable], expose: List[ExposedVariable]):
        self.expose = expose
        self.variables = variables
        self.file = file
        self.address = address


class InsertBranchAndLink:

    def __init__(self, address: HexAddress, value: str):
        self.value = value
        self.address = address



def parse_yaml(yaml):
    commands = []
    for payload_entry in yaml:
        cmd = payload_entry.get('cmd')
        if cmd == "insert_payload":
            address = HexAddress(payload_entry.get('address'))
            file = read_dump_file(payload_entry.get('file'))
            variables = payload_entry.get('variables', {})
            variables = [
                Variable(name, HexAddress(data['file_address']), HexAddress(data['value']), data['register'])
                for name, data in variables.items()
            ]

            expose = payload_entry.get('expose', {})
            expose = [
                ExposedVariable(name, HexAddress(data['file_address']))
                for name, data in expose.items()
            ]
            command = InsertPayloadCommand(address, file, variables, expose)
        elif cmd == "insert_asm":
            address = HexAddress(payload_entry.get('address'))
            value = payload_entry.get('value')
            command = InsertBranchAndLink(address, value)
            pass
        else:
            raise ValueError(f"Invalid cmd value : {cmd}")
            pass
        commands.append(command)

    return commands
