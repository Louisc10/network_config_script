# Network Configuration Script

This Python script automates the process of retrieving network information and configuring a static IP for the "Ethernet" network interface on a Windows system using the `netsh` command.

## Prerequisites

- Python 3.x
- `subprocess` and `re` modules (both are part of the Python standard library)
- Administrative privileges to run `netsh` commands on Windows

## Script Overview

The script performs the following actions:

1. **Sets the Ethernet Interface to DHCP**:
   The script first configures the "Ethernet" network interface to use DHCP (Dynamic Host Configuration Protocol) for automatic IP address assignment.

2. **Retrieves Network Information**:
   The script retrieves the current IP address, subnet mask, and default gateway of the "Ethernet" interface using the `netsh` command and regular expressions.

3. **Generates a Static IP Address**:
   Based on the retrieved IP address, the script generates a static IP address by replacing the last octet of the current IP address with a predefined `TARGET_IP` value (default: `150`).

4. **Sets the Static IP Address**:
   The script configures the "Ethernet" interface to use the generated static IP address, along with the retrieved subnet mask and gateway.

## Configuration

- **TARGET_IP**: The script defines a target static IP address (default value is `150`). This value is used to generate the last octet of the static IP address, while the first three octets are derived from the current IP address.

## Functions

- `run_command(command)`: Executes a shell command using `subprocess.run` and returns the output. If the command fails, an error message is printed.

- `get_network_info()`: Retrieves the current IP address, subnet mask, and gateway of the "Ethernet" interface by running the `netsh` command and extracting the relevant information using regular expressions.

- `set_static_ip(ip, subnet_mask, gateway)`: Configures the "Ethernet" interface to use a static IP address with the specified IP address, subnet mask, and gateway.

## Execution Flow

1. The script sets the "Ethernet" interface to DHCP mode to retrieve the current network configuration.
2. It then fetches the current IP address, subnet mask, and gateway using `netsh`.
3. If the network information is successfully retrieved, the script generates a static IP address by modifying the last octet of the current IP address.
4. The script then sets the "Ethernet" interface to use the new static IP address, along with the original subnet mask and gateway.
5. If the network information cannot be retrieved, the script prints an error message.

## Example Usage

```bash
python network_config.py
```

## Notes

- Ensure you have administrative privileges to run `netsh` commands on your Windows machine.
- The `TARGET_IP` value can be changed to modify the last octet of the generated static IP address.
- The script is designed for use on Windows systems where the network interface is named "Ethernet." If your interface is named differently, you will need to modify the interface name in the script.
- Language Dependency: This script assumes that the `netsh` command outputs information in French. Specifically, the script looks for French language terms like "Adresse IP", "masque", and "Passerelle par défaut". If your system uses a different language for `netsh` output, the script may not work as intended.

## License

This script is open-source and available for free use. Modify or distribute it as needed.
