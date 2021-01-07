"""
    Main program for getting an ip by anydesk.
    Run this script just someone try to connect to your PC.
"""
import wmi
import psutil

def get_ips() -> list:
    """ Getting the list of ips of anydesk """

    # Initializing the wmi constructor
    wmi_obj = wmi.WMI()
    ips = []

    # Iterating through all the running processes
    for process in wmi_obj.Win32_Process():

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

    return ips

def main() -> None:
    """ Main program """
    ips = get_ips()

    # printing ips
    if len(ips) > 0:
        for conn_ip in ips:
            print(f"Connection Found, IP: {conn_ip}")
    else:
        print('Anydesk is turned off or nobody is trying to connecting to your monitor...')


if __name__ == '__main__':
    main()
    input()
