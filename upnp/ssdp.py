#
#         Basic SSDP (Simple Service Discovery Protocol) implementation
#
#  This file is part of SimplyUPnP
#
#  Copyright (C) 2013  Matheus Silva Santos
#
#  SimplyUPnP is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SimplyUPnP is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with SimplyUPnP.  If not, see <http://www.gnu.org/licenses/>.
#

from constants import *
import platform as plat
import socket as s
import struct
import re


# As defined on section 1.3
def search(st_arg, timeout = 5, mx_arg = '1', ttl = SSDP['TTL'],
           ssdp_address = SSDP['IPV4_ADDR'], ssdp_port = SSDP['PORT']):
    
    # Create a socket
    s.setdefaulttimeout(timeout)
    socket = s.socket(s.AF_INET, s.SOCK_DGRAM, s.IPPROTO_UDP)
    socket.setsockopt(s.IPPROTO_IP, s.IP_MULTICAST_TTL, ttl)
    
    # Create the search request message
    message = 'M-SEARCH * HTTP/1.1\r\n' +\
              'HOST: ' + ssdp_address + ':' + str(ssdp_port) + '\r\n' +\
              'MAN: \"ssdp:discover\"\r\n' +\
              'MX: ' + mx_arg + '\r\n' +\
              'ST: ' + st_arg + '\r\n' +\
              'USER-AGENT: ' + plat.system() + '/' + plat.version() + ' ' +\
                           'UPnP/'+ UPNP['VERSION'] + ' ' +\
                           'SimplyUPnP/'+ LIB['VERSION'] +'\r\n\r\n'

    # print 'Searching for devices using this header: \n'
    # print message

    # Send the message through the socket
    socket.sendto(message, (ssdp_address, ssdp_port))

    # Loop checking what have answered to the request
    buffer_size = 1024
    devices = []
    while True:
        try:
            header, address = socket.recvfrom(buffer_size)
            # print address
            print header
            header = dict(re.findall("(?P<key>.*?):\s?(?P<value>.*?)\r\n", header))
            has_req = True
            for required_key in SSDP['REQUIRED_RESPONSE']:
                if required_key not in header:
                    # print required, 'is required header field \n'
                    has_req = False
                    break
            if has_req:
                devices.append(header)
        except s.timeout:
            # print 'Connection has timed out. \n'
            break

    socket.close()
    # print devices
    return devices


if __name__ == '__main__':
    search('ssdp:all')

