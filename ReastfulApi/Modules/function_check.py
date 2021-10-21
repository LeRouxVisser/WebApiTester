import xml.dom.minidom as xdm

def CheckType(packet):
    """
        Function will determine if packet is of type xml or json
    """
    packet_type = None
    if (isinstance(packet, dict)):
        packet_type = 'json'
    else:
        try:
            xdm.parseString(packet)
            packet_type = 'xml'
        except xdm.xml.parsers.expat.ExpatError:
            pass
    return packet_type

def is_intable(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
