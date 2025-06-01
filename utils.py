
ip_to_location = {
    "192.168.": "Office1",
    "10.": "Office2",
    "172.16.": "Office3",
    "172.17.": "Office4",
}

def get_internal_ip():
    import socket
    hostname = socket.gethostname()
    internal_ip = socket.gethostbyname(hostname)
    return internal_ip

def is_in_office():
    internal_ip = get_internal_ip()

    if not internal_ip:
        return False
    
    for tracked_prefix in ip_to_location.keys():
        if internal_ip.startswith(tracked_prefix):
            return True
    return False

def get_office_location():
    internal_ip = get_internal_ip()
    for prefix, location in ip_to_location.items():
        if internal_ip.startswith(prefix):
            return location
    return "Unknown"