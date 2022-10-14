import os
import sys
import wmi
import psutil
import requests

def get_ips() -> list:
    wmi_obj = wmi.WMI()
    ips = []

    # Iterating through all the running processes
    for process in wmi_obj.Win32_Process():
        try:
            if 'anydesk' in process.Name.lower():
                for conn in psutil.Process(process.ProcessId).connections():
                    if conn.status in ('SYN_SENT', 'ESTABLISHED'):  # Only connection packets
                        conn_ip = conn.raddr.ip
                        if conn.raddr.port != 80:
                            if not conn_ip.startswith('192.168.'):
                                if not conn_ip in ips:
                                    ips.append(conn_ip)
        except psutil.NoSuchProcess:
            pass

    return ips

def get_ip_info(conn_ip: str) -> dict:
    j = requests.get(f'http://ip-api.com/json/{conn_ip}').json()
    return dict(
        IP=conn_ip,
        Country=j.get('country', 'Unknown'),
        Region=j.get('regionName', 'Unknown'),
        City=j.get('city', 'Unknown'),
        ISP=j.get('isp', 'Unknown')
    )


def try_exit() -> None:
    """ Exit from the program """
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0) # pylint: disable=protected-access


def main() -> None:
    msg = 'Anydesk is turned off or noone is trying to connect to your monitor, retry... [CTRL+C to exit]'
    while True:
        try:
            ips = get_ips()
            print(' ' * len(msg), flush=False, end='\r')
               
            # Something found
            if len(ips) > 0:
                for conn_ip in ips:
                    print("Connection Found, infos:")
                    infos = get_ip_info(conn_ip)
                    for key, value in infos.items():
                        print(f'{key}: {value}')

            else:
                print(msg, flush=True, end='\r')
        except KeyboardInterrupt:
            print('\nProgram finished, exit...')
            try_exit()

        if len(ips) > 0:
            break


if __name__ == '__main__':
    main()
    input()
