from src.binarydump import BinaryDump
from src.hex_address import HexAddress
from src.patch_parser import InsertPayloadCommand, InsertBranchAndLink, Variable
from src.power_pc_assembler import PowerPCAssembler


def apply_variable(file: BinaryDump, variable: Variable):
    register = variable.register
    address = variable.value.to_int()
    high = HexAddress((address >> 16) & 0xFFFF)
    low = HexAddress(address & 0xFFFF)
    code = [
        f"lis {register},{high}",
        f"ori {register},{register},{low}"
    ]
    assembler = PowerPCAssembler()
    bytes = assembler.assemble_from_list(code)
    file.write_bytes(variable.file_address, bytes)
    # cmd.file.write_long(variable.file_address, variable.value.to_int())


def apply_patch(dump: BinaryDump, cmdList: {}):
    assembler = PowerPCAssembler()
    varlist = {}
    for cmd in cmdList:
        if isinstance(cmd, InsertPayloadCommand):
            # Add Variables into Payload:
            for variable in cmd.variables:
                apply_variable(cmd.file, variable)
            # Get variables of payload:
            for variable in cmd.expose:
                var_addr = variable.file_address + cmd.address
                varlist[variable.name] = var_addr
                pass
            # Add Payload into dump:
            dump.add_file_to_address(cmd.address, cmd.file)

            pass
        if isinstance(cmd, InsertBranchAndLink):
            asm_code = cmd.value
            for varname, varvalue in varlist.items():
                if isinstance(varvalue, HexAddress):
                    varvalue = varvalue.to_str()
                asm_code = asm_code.replace(varname, varvalue)
            asm_code = HexAddress(asm_code)
            code = assembler.generate_bl_instruction(cmd.address, asm_code)
            dump.write_bytes(cmd.address, code)
