# SimplyUPnP information
LIB = {
    'VERSION': '0.xxx',
}

# Implemented UPnP information
UPNP = {
    'VERSION': '1.1',
}

# Default values for SSDP, as defined on section 1.3 of official UPnP 1.1 specs
SSDP = {
    'IPV4_ADDR': '239.255.255.250',
    'PORT': 1900,
    'TTL': 2,
    'REQUIRED_RESPONSE': [
        'CACHE-CONTROL',
        'EXT',
        'LOCATION',
        'SERVER',
        'ST',
        'USN',
    ],
}
