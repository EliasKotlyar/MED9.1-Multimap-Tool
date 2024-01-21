from bitstring import BitArray

from src.hex_address import HexAddress


class PowerPCAssembler:
    def __init__(self):
        '''
        Initializes a PowerPCAssembler object with an empty list of instructions.
        '''
        self.instructions = []

    def generate_b_instruction(self, target_address):
        '''
        Generates a branch (b) instruction for the specified target address.

        Parameters:
        - target_address (int): The target address to branch to.

        Returns:
        - bytes: The assembled byte array for the branch instruction.
        '''
        opcode = 0x48000002
        offset = (target_address - 4) & 0x03FFFFFC
        instruction = opcode | offset

        # Convert the instruction to a byte array
        instruction_bytes = instruction.to_bytes(4, byteorder='big')

        return instruction_bytes

    def generate_bl_instruction(self, bl_address: HexAddress, target_address: HexAddress):
        bl_address = bl_address.to_int()
        target_address = target_address.to_int()
        # Calculate the relative offset
        relative_offset = (target_address - bl_address) / 4

        # Check if the offset is within the 24-bit signed range
        if relative_offset < -2 ** 23 or relative_offset > 2 ** 23 - 1:
            raise ValueError("Target address is out of range for a 24-bit offset.")

        # Set the opcode for BL instruction
        opcode = 18  # BL opcode in PowerPC assembly
        bitstring = BitArray(uint=0, length=32)
        opcode = BitArray(uint=opcode, length=6)
        bitstring.overwrite(opcode, 0)
        # Operand
        relative_offset = relative_offset
        operand = BitArray(int=relative_offset, length=24)
        bitstring.overwrite(operand, 6)
        # Set LK Bit:
        lk = BitArray(uint=1, length=1)
        bitstring.overwrite(lk, 31)

        return bitstring.tobytes()

    def assemble_from_list(self, lines: [str]):
        '''
        Assembles PowerPC assembly instructions from a list of strings.

        Parameters:
        - lines (list): List of PowerPC assembly instructions.

        Returns:
        - bytearray: The assembled bytecode as a bytearray.
        '''
        bytecode = bytearray()
        for line in lines:
            parts = line.replace(",", " ").strip().split(' ')
            opcode = parts[0]
            operands = parts[1:]

            if opcode == 'b':
                address = int(operands[0], 16)
                bytecode += self.generate_b_instruction(address)

            elif opcode == 'bl':
                address = HexAddress(operands[0])
                bytecode += self.generate_bl_instruction(address)
            elif opcode == 'lis':
                register = int(operands[0].replace("r", ""))
                address = HexAddress(operands[1])
                bytecode += self.generate_lis_instruction(register, address)
            elif opcode == 'ori':
                register1 = int(operands[0].replace("r", ""))
                register2 = int(operands[1].replace("r", ""))
                address = HexAddress(operands[2])
                bytecode += self.generate_ori_instruction(register1, register2, address)

            else:
                raise ValueError("Opcode '" + opcode + "' not found!")
            # Add more opcode handlers as needed...

        return bytes(bytecode)

    def generate_lis_instruction(self, register: int, value: HexAddress):
        value = value.to_int()
        # Ensure the register is valid (r0-r31 for PowerPC)
        if not (0 <= register <= 31):
            raise ValueError("Invalid register number. Must be between 0 and 31.")

        # Ensure the value fits within 16 bits (LIS instruction)
        if not (0 <= value <= 0xFFFF):
            raise ValueError("Invalid value. Must be a 16-bit unsigned integer.")

        opcode = 15
        bitstring = BitArray(uint=0, length=32)
        opcode = BitArray(uint=opcode, length=6)
        bitstring.overwrite(opcode, 0)
        operand = BitArray(uint=register, length=5)
        bitstring.overwrite(operand, 6)
        operand = BitArray(uint=value, length=16)
        bitstring.overwrite(operand, 16)
        return bitstring.tobytes()

    def generate_ori_instruction(self, register_target: int, register_source: int, value: HexAddress):
        value_int = value.to_int()
        # Ensure the registers are valid (r0-r31 for PowerPC)
        if not (0 <= register_target <= 31) or not (0 <= register_source <= 31):
            raise ValueError("Invalid register number. Must be between 0 and 31.")

        # Ensure the immediate value fits within 16 bits (ORI instruction)
        if not (0 <= value_int <= 0xFFFF):
            raise ValueError("Invalid immediate value. Must be a 16-bit unsigned integer.")

        opcode = 24
        bitstring = BitArray(uint=0, length=32)
        opcode = BitArray(uint=opcode, length=6)
        bitstring.overwrite(opcode, 0)
        operand = BitArray(uint=register_source, length=5)
        bitstring.overwrite(operand, 6)
        operand = BitArray(uint=register_target, length=5)
        bitstring.overwrite(operand, 11)
        operand = BitArray(uint=value_int, length=16)
        bitstring.overwrite(operand, 16)

        return bitstring.tobytes()


if __name__ == '__main__':
    ppc = PowerPCAssembler()
    # Lis:
    bytecode = ppc.generate_lis_instruction(3, HexAddress("0x1234"))
    assert bytecode.hex() == "3c601234", f"Assertiong failed: {bytecode.hex()}"
    # ori:
    bytecode = ppc.generate_ori_instruction(1, 2, HexAddress("0x0"))
    assert bytecode.hex() == "60410000", f"Assertiong failed: {bytecode.hex()}"
    bytecode = ppc.generate_ori_instruction(10, 13, HexAddress("0x0"))
    assert bytecode.hex() == "61aa0000", f"Assertiong failed: {bytecode.hex()}"
    # BL:
    bytecode = ppc.generate_bl_instruction(HexAddress("0x5bace8"), HexAddress("0x5bacec"))
    assert bytecode.hex() == "48000005", f"Assertiong failed: {bytecode.hex()}"

# 24 (dec) = 0x18 (hex) =
