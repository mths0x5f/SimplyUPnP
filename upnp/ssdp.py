#
# Basic SSDP (Simple Service Discovery Protocol) implementation
#   by Matheus Silva Santos (mths0x5f@gmail.com)
#
# As described in Official UPnP Specifications:
# http://www.upnp.org/specs/arch/UPnP-arch-DeviceArchitecture-v1.0-20080424.pdf
#

import socket
import re

def searchDevices(st_arg='upnp:rootdevice', timeout=10):
    
    socket.setdefaulttimeout(timeout) # Time spent searching for devices

    # Create a socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send search request through the socket
    # Please note that the address and port will "never" change,
    # as they are defined on UPnP specs and reserved by IANA.
    # Also, note that "ST" can vary to filter the results list.
    message = 'M-SEARCH * HTTP/1.1\r\n' +\
              'HOST: 239.255.255.250:1900\r\n' +\
              'MAN: \"ssdp:discover\"\r\n' +\
              'MX: 10\r\n' +\
              'ST: ' + st_arg + '\r\n\r\n'
    print message

    sock.sendto(message, ('239.255.255.250', 1900))
    
    # Loop checking what have answered to the request
    buffer_size = 1024
    devices = []
    while True:
        try:
            header, address = sock.recvfrom(buffer_size)
            print header
            header = dict(re.findall("(?P<key>.*?):(?P<value>.*?)\r\n", header))
            devices.append(header)
        except socket.timeout:
            print 'Connection has timed out.'
            break

    print devices
    return devices


# Just in case someone calls it directly, you know, for fun.
if __name__ == '__main__':
    searchDevices()
