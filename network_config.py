import re
import subprocess

TARGET_IP = '150'

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        result.check_returncode()
        print(f"Commande exécutée avec succès:\n{result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Échec de la commande avec l'erreur: {e.stderr}")
        return None

def get_network_info():
    result = run_command('netsh interface ip show config "Ethernet"')
        
    ip_match = re.search(r'Adresse IP\s*:\s*(\d+\.\d+\.\d+\.\d+)', result)
    subnet_mask_match = re.search(r'Préfixe de sous-réseau\s*:\s*\d+\.\d+\.\d+\.\d+/\d+\s*\(masque\s*(\d+\.\d+\.\d+\.\d+)\)', result)
    gateway_match = re.search(r'Passerelle par défaut\s*:\s*(\d+\.\d+\.\d+\.\d+)', result)

    if ip_match and subnet_mask_match and gateway_match:
        return ip_match.group(1), subnet_mask_match.group(1), gateway_match.group(1)
    return None, None, None

def set_static_ip(ip, subnet_mask, gateway):
    static_ip_command = f'netsh interface ip set address "Ethernet" static {ip} {subnet_mask} {gateway}'
    run_command(static_ip_command)

if __name__ == '__main__':
    print('Réglage de l\'Ethernet sur DHCP...')
    run_command('netsh interface ip set address "Ethernet" dhcp')

    print('Obtention des informations réseau...')
    ip, subnet_mask, gateway = get_network_info()
    if ip and subnet_mask and gateway:
        print(f'Mon adresse IP: {ip}')
        print(f'Masque de sous-réseau: {subnet_mask}')
        print(f'Passerelle: {gateway}')
        
        subnet = '.'.join(ip.split('.')[:3])
        static_ip = f'{subnet}.{TARGET_IP}'

        set_static_ip(static_ip, subnet_mask, gateway)
        print(f'Adresse IP statique définie sur: {static_ip}')
    else:
        print('Échec de la récupération des informations réseau depuis DHCP')
        
    run_command('exit')