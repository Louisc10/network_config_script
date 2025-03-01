import re
import subprocess

TARGET_IP = '150'

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"Command failed with error: {result.stderr}")
    return result.stdout

def get_network_info():
    result = run_command('netsh interface ip show config "Ethernet"')
    print("Command output:", result)

    ip_match = re.search(r'Adresse IP\s*:\s*(\d+\.\d+\.\d+\.\d+)', result)
    subnet_mask_match = re.search(r'(masque\s*\d+\.\d+\.\d+\.\d+)', result)
    gateway_match = re.search(r'Passerelle par défaut\s*:\s*(\d+\.\d+\.\d+\.\d+)', result)

    if ip_match and subnet_mask_match and gateway_match:
        return ip_match.group(1), subnet_mask_match.group(1), gateway_match.group(1)
    return None, None, None

def set_static_ip(ip, subnet_mask, gateway):
    static_ip_command = f'netsh interface ip set address "Ethernet" static {ip} {subnet_mask} {gateway}'
    run_command(static_ip_command)

if __name__ == '__main__':
    print('Setting Ethernet to DHCP...')
    run_command('netsh interface ip set address "Ethernet" dhcp')

    print('Getting network information...')
    ip, subnet_mask, gateway = get_network_info()
    if ip and subnet_mask and gateway:
        print(f'My IP Address: {ip}')
        print(f'Subnet Mask: {subnet_mask}')
        print(f'Gateway: {gateway}')
        
        subnet = '.'.join(ip.split('.')[:3])
        static_ip = f'{subnet}.{TARGET_IP}'

        set_static_ip(static_ip, subnet_mask, gateway)
        print(f'Static IP set to: {static_ip}')
    else:
        print('Failed to retrieve network information from DHCP')
        
    run_command('exit')