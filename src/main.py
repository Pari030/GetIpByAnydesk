"""
    Main program for getting an ip by anydesk.
"""
import os
import sys
import wmi
import psutil

from requests import get

def get_ips() -> list:
    """ Getting the list of ips of anydesk """

    # Initializing the wmi constructor
    wmi_obj = wmi.WMI()
    ips = []

    # Iterating through all the running processes
    for process in wmi_obj.Win32_Process():

        try:
            # Getting anydesk
            if 'anydesk' in process.Name.lower():

                # Iterating process connections
                for conn in psutil.Process(process.ProcessId).connections():

                    # Getting only SYN SENT connections
                    if conn.status in ('SYN_SENT', 'ESTABLISHED'):

                        # Getting remote address ip and port
                        conn_ip = conn.raddr.ip

                        # Port 80 is anydesk server
                        if conn.raddr.port != 80:

                            # Check if is the local ip LOL
                            if not conn_ip.startswith('192.168.'):

                                # Checking if the ip is duplicated
                                if not conn_ip in ips:

                                    # Adding ip to the ips list
                                    ips.append(f"{conn_ip}")
        except psutil.NoSuchProcess:
            pass

    return ips

def get_ip_info(conn_ip: str) -> dict:
    """ Get information about an IP """

    info_obj = get(f'http://ip-api.com/json/{conn_ip}').json()

    country = info_obj.get('country', 'Unknown')
    region = info_obj.get('regionName', 'Unknown')
    city = info_obj.get('city', 'Unknown')
    isp = info_obj.get('isp', 'Unknown')

    return dict(
            IP=conn_ip,
            Country=country,
            Region=region,
            City=city,
            ISP=isp
        )


def try_exit() -> None:
    """ Exit from the program """
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0) # pylint: disable=protected-access


def main() -> None:
    """ Main program """
    msg = 'Anydesk is turned off or noone is trying to connect to your monitor, retry... [CTRL+C to exit]'
    while True:
        try:
            ips = get_ips()
            print(' ' * len(msg), flush=False, end='\r')

            # printing ips
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
