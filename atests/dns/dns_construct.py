from construct import Int16ub, BitStruct, Flag, BitsInteger, Int32ub, Int8ub, RepeatUntil, PascalString, Array, CString, Bytes, Struct, this, obj_

dns_payload_tcp = Struct(
    "length" / Int16ub,            # Transaction ID (16 bits)
    "transaction_id" / Int16ub,            # Transaction ID (16 bits)
    "flags" / BitStruct(                   # Flags (16 bits)
        "qr" / Flag,                       # Query (0) or Response (1)
        "opcode" / BitsInteger(4),         # Opcode (4 bits)
        "aa" / Flag,                       # Authoritative Answer (1 bit)
        "tc" / Flag,                       # Truncated (1 bit)
        "rd" / Flag,                       # Recursion Desired (1 bit)
        "ra" / Flag,                       # Recursion Available (1 bit)
        "z" / BitsInteger(3),              # Reserved (3 bits)
        "rcode" / BitsInteger(4),          # Response Code (4 bits)
    ),
    "qdcount" / Int16ub,                   # Number of entries in Question section
    "ancount" / Int16ub,                   # Number of entries in Answer section
    "nscount" / Int16ub,                   # Number of entries in Authority section
    "arcount" / Int16ub,                   # Number of entries in Additional section

    "questions" / Array(this.qdcount, Struct(
        "qname" / RepeatUntil(obj_=="''", PascalString(Int8ub, "ascii")),        # Domain name being queried
        "qtype" / Int16ub,                 # Query type
        "qclass" / Int16ub,                # Query class
    )),
    "answers" / Array(this.ancount, Struct(
        "name" / Int16ub,         # Name for the answer
        "type" / Int16ub,                  # Type of the answer
        "class" / Int16ub,                 # Class of the answer
        "ttl" / Int32ub,                   # Time to live
        "rdlength" / Int16ub,              # Length of the RDATA
        "rdata" / Array(this.rdlength, Int8ub),    # Actual data (e.g., IP address)
    )),
    "authority"    / Array(this.nscount, Struct(
        "name"     / CString("ascii"),         # Name of the authority record
        "type"     / Int16ub,                  # Type of the record
        "class"    / Int16ub,                 # Class of the record
        "ttl"      / Int32ub,                   # Time to live
        "rdlength" / Int16ub,              # Length of the RDATA
        "rdata"    / Bytes(this.rdlength),    # Actual data (e.g., nameserver address)
    )),
    "additional" / Array(this.arcount, Struct(
        "name" / CString("ascii"),         # Name of the additional record
        "type" / Int16ub,                  # Type of the record
        "class" / Int16ub,                 # Class of the record
        "ttl" / Int32ub,                   # Time to live
        "rdlength" / Int16ub,              # Length of the RDATA
        "rdata" / Array(this.rdlength, Int8ub),    # Actual data (e.g., IP address of a nameserver)
    )),
).compile()
dns_payload_tcp.name = "dns_payload_tcp"

dns_payload_udp = Struct(
    "transaction_id" / Int16ub,            # Transaction ID (16 bits)
    "flags" / BitStruct(                   # Flags (16 bits)
        "qr" / Flag,                       # Query (0) or Response (1)
        "opcode" / BitsInteger(4),         # Opcode (4 bits)
        "aa" / Flag,                       # Authoritative Answer (1 bit)
        "tc" / Flag,                       # Truncated (1 bit)
        "rd" / Flag,                       # Recursion Desired (1 bit)
        "ra" / Flag,                       # Recursion Available (1 bit)
        "z" / BitsInteger(3),              # Reserved (3 bits)
        "rcode" / BitsInteger(4),          # Response Code (4 bits)
    ),
    "qdcount" / Int16ub,                   # Number of entries in Question section
    "ancount" / Int16ub,                   # Number of entries in Answer section
    "nscount" / Int16ub,                   # Number of entries in Authority section
    "arcount" / Int16ub,                   # Number of entries in Additional section

    "questions" / Array(this.qdcount, Struct(
        "qname" / RepeatUntil(obj_=="''", PascalString(Int8ub, "ascii")),        # Domain name being queried
        "qtype" / Int16ub,                 # Query type
        "qclass" / Int16ub,                # Query class
    )),
    "answers" / Array(this.ancount, Struct(
        "name" / Int16ub,         # Name for the answer
        "type" / Int16ub,                  # Type of the answer
        "class" / Int16ub,                 # Class of the answer
        "ttl" / Int32ub,                   # Time to live
        "rdlength" / Int16ub,              # Length of the RDATA
        "rdata" / Array(this.rdlength, Int8ub),    # Actual data (e.g., IP address)
    )),
    "authority"    / Array(this.nscount, Struct(
        "name"     / CString("ascii"),         # Name of the authority record
        "type"     / Int16ub,                  # Type of the record
        "class"    / Int16ub,                 # Class of the record
        "ttl"      / Int32ub,                   # Time to live
        "rdlength" / Int16ub,              # Length of the RDATA
        "rdata"    / Bytes(this.rdlength),    # Actual data (e.g., nameserver address)
    )),
    "additional" / Array(this.arcount, Struct(
        "name" / CString("ascii"),         # Name of the additional record
        "type" / Int16ub,                  # Type of the record
        "class" / Int16ub,                 # Class of the record
        "ttl" / Int32ub,                   # Time to live
        "rdlength" / Int16ub,              # Length of the RDATA
        "rdata" / Array(this.rdlength, Int8ub),    # Actual data (e.g., IP address of a nameserver)
    )),
).compile()
dns_payload_udp.name = "dns_payload_udp"


exampleRequestRoboconUdp = {'transaction_id': 26331,
 'flags': dict(qr=False, opcode=0, aa=False, tc=False, rd=True, ra=False, z=2, rcode=0),
 'qdcount': 1,
 'ancount': 0,
 'nscount': 0,
 'arcount': 1,
 'questions': [{'qname': [u'robocon', u'io', u""],
                'qtype': 1,
                'qclass': 1}],
 'answers': [],
 'authority': [],
 'additional': [{'name': '',
                 'type': 41,
                 'class': 1200,
                 'ttl': 0,
                 'rdlength': 0,
                 'rdata': b''}]}

exampleRequestRoboconTcp = {
    'length': 39,
    'transaction_id': 26331,
    'flags': dict(qr=False, opcode=0, aa=False, tc=False, rd=True, ra=False, z=2, rcode=0),
    'qdcount': 1,
    'ancount': 0,
    'nscount': 0,
    'arcount': 1,
    'questions': [{'qname': [u'robocon', u'io', u""],
                   'qtype': 1,
                   'qclass': 1}],
    'answers': [],
    'authority': [],
    'additional': [{'name': '',
                    'type': 41,
                    'class': 1200,
                    'ttl': 0,
                    'rdlength': 0,
                    'rdata': b''}]}
