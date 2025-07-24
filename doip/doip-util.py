import re

def change_physical_addresses(new_addr: int):
    """
    modify the physical addresses in the DoIP configuration file (test.toml).
    eg. physical_addresses = [0xabcd] -> physical_addresses = [new_addr]
    """
    config_file = "test.toml"

    # Read the file content
    with open(config_file, "r") as f:
        content = f.read()

    # Replace the physical addresses array using regex
    modified_content = re.sub(
        r'physical_addresses\s*=\s*\[(.*?)\]',
        f'physical_addresses = [{new_addr}]',
        content
    )

    # Write back to file
    with open(config_file, "w") as f:
        f.write(modified_content)