"""
DHCP Server using Asyncio

This program is a simple DHCP Server that listens for DHCP messages on a
specific network interface and responds with basic DHCP options like IP
address, subnet mask, and gateway.

Author: Kris Armstrong
Date: 1/1/2023
License: Apache 2.0

PEP 8 Compliance:
- 4 spaces per indentation level
- Maximum line length of 79 characters
"""

import asyncio
import ipaddress
import struct
import socket

# DHCP message opcodes
BOOTREQUEST = 1
BOOTREPLY = 2

# DHCP message options
DHCP_MESSAGE_TYPE = 53
DHCP_MESSAGE_TYPE_OFFER = 2

DHCP_SERVER_IDENTIFIER = 54

DHCP_SUBNET_MASK = 1
DHCP_ROUTER = 3
DHCP_IP_ADDRESS_LEASE_TIME = 51

# DHCP message format
DHCP_FMT = "!4B4B4B4B4B16s64s128sI4s6s16s6s"
DHCP_OPTIONS_FMT = "!BB"

# DHCP message fields
DHCP_FIELDS = [
    "op", "htype", "hlen", "hops", "xid", "secs", "flags", "ciaddr",
    "yiaddr", "siaddr", "giaddr", "chaddr", "sname", "file", "magic",
    "options"
]


async def dhcp_server(interface):
    """
    Run the DHCP Server on the specified network interface.

    Args:
        interface (str): The network interface to listen on.

    Returns:
        None
    """
    # Set up the DHCP server socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((interface, 67))

        while True:
            data, addr = await loop.sock_recvfrom(sock, 1024)

            dhcp_message = unpack_dhcp_message(data)
            dhcp_message_type = dhcp_message.get(DHCP_MESSAGE_TYPE)

            if dhcp_message_type == BOOTREQUEST:
                dhcp_options = {
                    DHCP_MESSAGE_TYPE: DHCP_MESSAGE_TYPE_OFFER,
                    DHCP_SERVER_IDENTIFIER: socket.inet_aton(interface),
                    DHCP_SUBNET_MASK: socket.inet_aton("255.255.255.0"),
                    DHCP_ROUTER: socket.inet_aton("192.168.0.1"),
                    DHCP_IP_ADDRESS_LEASE_TIME: struct.pack("!I", 86400)
                }

                dhcp_message_reply = pack_dhcp_message(
                    BOOTREPLY,
                    dhcp_message["chaddr"],
                    dhcp_options,
                    dhcp_message["xid"]
                )

                sock.sendto(dhcp_message_reply, ("<broadcast>", 68))


def unpack_dhcp_message(data):
    """
    Unpack a DHCP message from binary data.

    Args:
        data (bytes): The binary data containing the DHCP message.

    Returns:
        dict: A dictionary containing the DHCP message fields and options.
    """
    dhcp_fields = struct.unpack(DHCP_FMT, data)
    dhcp_options = {}

    options = dhcp_fields[-1]
    options_offset = 0

    while options[options_offset] != 255:
        option_code = options[options_offset]
        option_len = options[options_offset + 1]
        option_data = options[options_offset + 2:options_offset + 2 + option_len]

        dhcp_options[option_code] = option_data

        options_offset += option_len + 2

    return dict(zip(DHCP_FIELDS, dhcp_fields[:-1]) + [("options", dhcp_options)])

 
def pack_dhcp_message(op, chaddr, options, xid):
    """
    Pack a DHCP message from a dictionary of message fields and options.

    Args:
        op (int): The DHCP message opcode (BOOTREQUEST or BOOTREPLY).
        chaddr (bytes): The client hardware address.
        options (dict): A dictionary containing the DHCP message options.
        xid (int): The DHCP transaction ID.

    Returns:
        bytes: A binary string containing the packed DHCP message.
    """
    packed_options = b""

    for option_code, option_data in options.items():
        packed_options += struct.pack(DHCP_OPTIONS_FMT, option_code, len(option_data)) + option_data

    packed_options += b"\xff"

    dhcp_fields = [
        op, 1, len(chaddr), 0, xid, 0, 0, 0, 0, 0, 0, chaddr, b"", b"", b"\x63\x82\x53\x63",
        packed_options
    ]

    return struct.pack(DHCP_FMT, *dhcp_fields)
