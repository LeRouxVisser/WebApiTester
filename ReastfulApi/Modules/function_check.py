import xml.dom.minidom as xdm
def CheckType(packet):
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