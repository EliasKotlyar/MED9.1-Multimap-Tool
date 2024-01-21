from src.dump_file import read_dump_file, write_dump_file
from src.ecuid import read_ecu_id
from src.patch_apply import apply_patch
from src.patch_parser import parse_yaml
from src.yml import read_yaml_file

filename = "1Q0907115C_0040.bin"
patchname = "mapswitch.yml"
dump = read_dump_file(filename)
# Analyse File:
ecuId = read_ecu_id(dump)
# Check for a definition file for that particlar ECU:
variants_filename = "patches/" + ecuId.vag_part_number + "_" + ecuId.vag_sw_version + "/" + patchname
patch = read_yaml_file(variants_filename)
cmd_list = parse_yaml(patch)
apply_patch(dump, cmd_list)
# Write file:

newfile_name = filename[:-4] + "_mapswitch.bin"
write_dump_file(newfile_name, dump)
