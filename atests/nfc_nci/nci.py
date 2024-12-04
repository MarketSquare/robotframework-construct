import serial
import select
from construct import Struct, Int8ub, Bytes, BitStruct, BitsInteger, this, Byte, Enum, Switch, Const, Array, Int16ub, If


_serial_connection = None

def open_nci_connection_via_uart(device: str, baudrate: int):
    """
    Opens a connection to a NCI device via UART.

    Returns a tuple of two file objects, first one for reading and second one for writing.
    """
    global _serial_connection
    _serial_connection = serial.Serial(device, baudrate, timeout=1)
    return (open(_serial_connection.fd, "rb", buffering=0, closefd=False), open(_serial_connection.fd, "wb", buffering=0, closefd=False),)

def close_nci_connection():
    """
    Closes the NCI connection by closing the serial connection.
    """
    global _serial_connection
    if _serial_connection and _serial_connection.is_open:
        _serial_connection.close()
    else:
        raise Exception("NCI connection is not open")

def wait_for_data_from_nci(timeout: float = 1.0):
    """
    Waits for data from the NCI device.

    Uses the select module to wait for data to be available on the serial connection.
    Raises an exception if the NCI connection is not open.
    """
    global _serial_connection
    if _serial_connection and _serial_connection.is_open:
        assert select.select([_serial_connection], [], [], timeout)[0], "Timeout while waiting for data from NCI device"
    else:
        raise Exception("NCI connection is not open")

MT = Enum(BitsInteger(3), # Aka Message Type
          DATA=0,
          ControlPacketCommand=1,
          ControlPacketResponse=2,
          ControlPacketNotification=3)

PBF = Enum(BitsInteger(1), # Aka Packet Boundary Flag
           endOfMessage=0,
           segment=1)

GID = Enum(BitsInteger(4),
              CORE=0,
              RF=1,
              NFCEE=2,
              Proprietary=0xF)

OID_NCI_Core = Enum(BitsInteger(6),
                    CORE_RESET=0,
                    CORE_INIT=1,
                    CORE_SET_CONFIG=2,
                    CORE_GET_CONFIG=3,
                    CORE_CONN_CREATE=4,
                    CORE_CONN_CLOSE=5,
                    CORE_CONN_CREDITS=6,
                    CORE_GENERIC_ERROR=7,
                    CORE_INTERFACE_ERROR=8,
                    )

OID_RF_Management = Enum(BitsInteger(6),
                         RF_DISCOVER_MAP=0,
                         RF_SET_LISTEN_MODE_ROUTING=1,
                         RF_GET_LISTEN_MODE_ROUTING=2,
                         RF_DISCOVER=3,
                         RF_DISCOVER_SELECT=4,
                         RF_INTF_ACTIVATED=5,
                         RF_DEACTIVATE=6,
                         RF_FIELD_INFO=7,
                         RF_T3T_POLLING=8,
                         RF_NFCEE_ACTION=9,
                         RF_NFCEE_DISCOVERY_REQ=10,
                         RF_PARAMETER_UPDATE=11,
                         )

OID_NFCEE_Management = Enum(BitsInteger(6),
                            NFCEE_DISCOVER=0,
                            NFCEE_MODE_SET=1,
                            )

CORE_RESET_CMD = Enum(Byte,
                      KEEP_CONFIGURATION=0,
                      RESET_CONFIGURATION=1)

CORE_RESET_RSP_STATUS = Enum(Byte,
                      STATUS_OK=0x00,
                      STATUS_REJECTED=0x01,
                      STATUS_RF_FRAME_CORRUPTED=0x02,
                      STATUS_FAILED=0x03,
                      STATUS_NOT_INITIALIZED=0x04,
                      STATUS_SYNTAX_ERROR=0x05,
                      STATUS_SEMANTIC_ERROR=0x06,
                      STATUS_INVALID_PARAM=0x09,
                      STATUS_MESSAGE_SIZE_EXCEEDED=0x0A,
                      DISCOVERY_ALREADY_STARTED=0xA0,
                      DISCOVERY_TARGET_ACTIVATION_FAILED=0xA1,
                      DISCOVERY_TEAR_DOWN=0xA2,
                      RF_TRANSMISSION_ERROR=0xB0,
                      RF_PROTOCOL_ERROR=0xB1,
                      RF_TIMEOUT_ERROR=0xB2,
                      NFCEE_INTERFACE_ACTIVATION_FAILED=0xC0,
                      NFCEE_TRANSMISSION_ERROR=0xC1,
                      NFCEE_PROTOCOL_ERROR=0xC2,
                      NFCEE_TIMEOUT_ERROR=0xC3) # Table 94


RF_Technology = Enum(Byte,
                     NFC_A_PASSIVE_POLL_MODE        = 0x00,
                     NFC_B_PASSIVE_POLL_MODE        = 0x01,
                     NFC_F_PASSIVE_POLL_MODE        = 0x02,
                     NFC_A_ACTIVE_POLL_MODE         = 0x03,
                     RFU                            = 0x04,
                     NFC_F_ACTIVE_POLL_MODE         = 0x05,
                     NFC_15693_PASSIVE_POLL_MODE    = 0x06,
                     NFC_A_PASSIVE_LISTEN_MODE      = 0x80,
                     NFC_B_PASSIVE_LISTEN_MODE      = 0x81,
                     NFC_F_PASSIVE_LISTEN_MODE      = 0x82,
                     NFC_A_ACTIVE_LISTEN_MODE       = 0x83,
                     NFC_F_ACTIVE_LISTEN_MODE       = 0x85,
                     NFC_15693_PASSIVE_LISTEN_MODE  = 0x86) # Table 96

RF_Discover_Frequency = Enum(Byte,
                             RFU=0x00,
                             EVERY_DISCOVERY=0x01)

GENERIC_STATUS_CODE = Enum(Byte,
                              STATUS_OK                          = 0x00,
                              STATUS_REJECTED                    = 0x01,
                              STATUS_RF_FRAME_CORRUPTED          = 0x02,
                              STATUS_FAILED                      = 0x03,
                              STATUS_NOT_INITIALIZED             = 0x04,
                              STATUS_SYNTAX_ERROR                = 0x05,
                              STATUS_SEMANTIC_ERROR              = 0x06,
                              STATUS_INVALID_PARAM               = 0x09,
                              STATUS_MESSAGE_SIZE_EXCEEDED       = 0x0A,
                              DISCOVERY_ALREADY_STARTED          = 0xA0,
                              DISCOVERY_TARGET_ACTIVATION_FAILED = 0xA1,
                              DISCOVERY_TEAR_DOWN                = 0xA2,
                              RF_TRANSMISSION_ERROR              = 0xB0,
                              RF_PROTOCOL_ERROR                  = 0xB1,
                              RF_TIMEOUT_ERROR                   = 0xB2,
                              NFCEE_INTERFACE_ACTIVATION_FAILED  = 0xC0,
                              NFCEE_TRANSMISSION_ERROR           = 0xC1,
                              NFCEE_PROTOCOL_ERROR               = 0xC2,
                              NFCEE_TIMEOUT_ERROR                = 0xC3)

RF_PROTOCOL = Enum(Byte,
                   PROTOCOL_UNDETERMINED = 0x00,
                   PROTOCOL_T1T          = 0x01,
                   PROTOCOL_T2T          = 0x02,
                   PROTOCOL_T3T          = 0x03,
                   PROTOCOL_ISO_DEP      = 0x04,
                   PROTOCOL_NFC_DEP      = 0x05) # Table 98

RF_DISCOVER_NTF_RF_DISCOVERY_RF_ID = Enum(
    Int8ub,
    RFU_0=0,  # RFU (Value 0)
    RFU_255=255  # RFU (Value 255)
) # Table 53

CONFIGURATION_STATUS = Enum(Byte,NCI_RF_CONFIGURATION_KEPT=0,
                                 NCI_RF_CONFIGURATION_RESET=1) # Table 7

NCI_VERSION = Enum(Byte, NCI_VERSION_1_0=0x10,
                         NCI_VERSION_2_0=0x20) # Table 6 

CORE_RESET_NTF_STATUS_REASON_CODE = Enum(Byte, UNSPECIFIED=0x00,
                                               CORE_RESET_TRIGGERED=0x01)

RF_DISCOVER_CMD_PAYLOAD = Struct("NumInterfaces" / Byte,
                                 "RF_Discover_Map" / Array(this.NumInterfaces, Struct("RF_Technology_and_Mode"  / RF_Technology,
                                                                                      "RF_Discover_Frequency"   / Int8ub)))
RF_DISCOVER_RSP_PAYLOAD = Struct("Status" / GENERIC_STATUS_CODE)

RF_DISCOVER_NTF_PAYLOAD = Struct("NumTargets" / Int8ub,
                                 "Payload"    / Bytes(this._.payload_length - 1))

NFCParameterStruct = Struct(
    "SENS_RES_Response" / Bytes(2),  # 2 Octets, Defined in [DIGITAL]
    
    "NFCID1_Length" / Enum(
        Int8ub,
        NOT_AVAILABLE=0x00,  # If no NFCID1 parameter is available
        LENGTH_4=0x04,       # Valid length 4 octets
        LENGTH_7=0x07,       # Valid length 7 octets
        LENGTH_10=0x0A,      # Valid length 10 octets
    ),
    
    "NFCID1" / Switch(
        this.NFCID1_Length,
        {
            0x04: Bytes(4),
            0x07: Bytes(7),
            0x0A: Bytes(10),
        },
        default=None  # If the length is invalid (RFU or unavailable)
    ),

    "SEL_RES_Response_Length" / Enum(
        Int8ub,
        NO_RESPONSE=0x00,  # If no SEL_RES Response is available
        LENGTH_1=0x01,     # Valid length 1 octet
        RFU=0xFF           # Reserved for Future Use
    ),
    
    "SEL_RES_Response" / Switch(
        this.SEL_RES_Response_Length,
        {
            0x01: Bytes(1)
        },
        default=None  # If the length is invalid (RFU or unavailable)
    )
)

NFCC_FEATURES = Struct("Octet_0" / BitStruct("RFU"                            / BitsInteger(5), 
                                             "DiscoverConfigurationmode"      / Enum(BitsInteger(2), 
                                                                                     SINGLDE_DH=0,
                                                                                     MULTI_NFCEEs=1),
                                             "DiscoverFrequencyConfiguration" / Enum(BitsInteger(1),
                                                                                     IGNORED=0,
                                                                                     RF_DISCOVER_CMD_SUPPORTED=1)),
                       "Octet_1" / BitStruct("RFU"                      / BitsInteger(4), 
                                             "AID_BASED_ROUTING"        / BitsInteger(1),
                                             "PROTOCOL_BASED_ROUTING"   / BitsInteger(1),
                                             "TECHNOLOGY_BASED_ROUTING" / BitsInteger(1),
                                             "RFU"                      / BitsInteger(1)),
                       "Octet_2" / BitStruct("RFU"                         / BitsInteger(6),
                                             "SWITCH_OFF_STATE_SUPPORTED"  / Enum(BitsInteger(1)),
                                             "BATTERY_OFF_STATE_SUPPORTED" / Enum(BitsInteger(1))),
                       "Octet_3" / BitStruct("RFU" / BitsInteger(8)))

RF_INTERFACES = Enum(Byte,
                     NFCEE_Direct_RF_Interface  = 0x00,
                     Frame_RF_Interface         = 0x01,
                     ISO_DEP_RF_Interface       = 0x02,
                     NFC_DEP_RF_Interface       = 0x03,) # Table 99

CORE_INIT_CMD_PAYLOAD = Struct("ConstValue"       / Const(b"\x00\x00"))

CORE_INIT_RSP_PAYLOAD = Struct("Status"                           / CORE_RESET_RSP_STATUS,
                               "NFCC_Features"                    / NFCC_FEATURES,
                               "NumInterfaces"                    / Int8ub,
                               "SupportedInterfaces"              / Array(this.NumInterfaces, RF_INTERFACES),
                               "Max_Logical_Connections"          / Int8ub,
                               "Max_Routing_Table_Size"           / Int16ub,
                               "Max_Control_Package_Payload_Size" / Int8ub,
                               "Max_Size_for_Large_Parameters"    / Int8ub,
                               "Manufacture_ID"                   / Int8ub,
                               "Manufacturer_specific_info"       / Bytes(4))

CORE_RESET_RSP = Struct("Status"               / If(this._.payload_length>=1, CORE_RESET_RSP_STATUS),
                        "NCI_Version"          / If(this._.payload_length>=2, NCI_VERSION),
                        "ConfigurationStatus"  / If(this._.payload_length>=3, CONFIGURATION_STATUS),
                        "padding"              / If(this._.payload_length> 3, Bytes(this._.payload_length-3)))

CORE_RESET_NTF = Struct("Reason"              / CORE_RESET_NTF_STATUS_REASON_CODE,
                        "ConfigurationStatus" / CONFIGURATION_STATUS,
                        "padding"              / If(this._.payload_length> 2, Bytes(this._.payload_length-2)))

NCI_DATA_PACKET = Struct(
    "header"            / BitStruct(
        "MT"            / MT,
        "PBF"           / PBF,
        "ConnID"        / BitsInteger(4),
        "RFU"           / Byte,  
        "PayloadLength" / Byte
    ),
    "payload_length" / Int8ub,
    "payload" / Bytes(this.payload_length)
)

CORE_RESET_CMD_PAYLOAD = Struct("ResetType" / CORE_RESET_CMD)

NCI_CONTROL_PACKET = Struct(
    "header" / BitStruct("MT" / MT,
                         "PBF" / PBF,
                         "GID" / GID,
                         "RFU" / BitsInteger(2),
                         "OID" / Switch(this.GID, {GID.CORE: OID_NCI_Core, GID.RF: OID_RF_Management, GID.NFCEE: OID_NFCEE_Management})),
    "payload_length" / Int8ub,
    "payload" / Switch((this.header.MT, this.header.GID, this.header.OID,), {(MT.ControlPacketCommand,      GID.CORE, OID_NCI_Core.CORE_RESET,):         CORE_RESET_CMD_PAYLOAD,
                                                                             (MT.ControlPacketResponse,     GID.CORE, OID_NCI_Core.CORE_RESET,):         CORE_RESET_RSP,
                                                                             (MT.ControlPacketNotification, GID.CORE, OID_NCI_Core.CORE_RESET,):         CORE_RESET_NTF,
                                                                             (MT.ControlPacketCommand,      GID.CORE, OID_NCI_Core.CORE_INIT,):          CORE_INIT_CMD_PAYLOAD,
                                                                             (MT.ControlPacketResponse,     GID.CORE, OID_NCI_Core.CORE_INIT,):          CORE_INIT_RSP_PAYLOAD,
                                                                             (MT.ControlPacketCommand,      GID.RF, OID_RF_Management.RF_DISCOVER,):     RF_DISCOVER_CMD_PAYLOAD,
                                                                             (MT.ControlPacketResponse,     GID.RF, OID_RF_Management.RF_DISCOVER,):    RF_DISCOVER_RSP_PAYLOAD,
                                                                             (MT.ControlPacketNotification, GID.RF, OID_RF_Management.RF_DISCOVER,):    RF_DISCOVER_NTF_PAYLOAD,
                                                                             })).compile()


NFC_RST_CMD=   {"header": {"MT": MT.ControlPacketCommand,
                                 "PBF": 0, 
                                 "GID": GID.CORE,
                                 "RFU": 0, 
                                 "OID": OID_NCI_Core.CORE_RESET}, 
                      "payload_length": 1,
                      "payload": {"ResetType": CORE_RESET_CMD.RESET_CONFIGURATION},
                      "padding": b""}

NFC_INIT_CMD=   {"header": {"MT": MT.ControlPacketCommand,
                                 "PBF": 0, 
                                 "GID": GID.CORE,
                                 "RFU": 0, 
                                 "OID": OID_NCI_Core.CORE_INIT}, 
                      "payload_length": 2,
                      "payload": {"ConstValue": b"\x00\x00"},
                      "padding": b""}



NCI_DISCVER_CMD = {"header": {"MT": MT.ControlPacketCommand,
                                  "PBF": 0,
                                  "GID": GID.RF,
                                  "RFU": 0,
                                  "OID": OID_RF_Management.RF_DISCOVER},
                       "payload_length": 13,
                       "payload": {"NumInterfaces": 6,
                                   "RF_Discover_Map": [{"RF_Technology_and_Mode":RF_Technology.NFC_A_PASSIVE_POLL_MODE, 
                                                        "RF_Discover_Frequency": 2},
                                                        {"RF_Technology_and_Mode":RF_Technology.NFC_B_PASSIVE_POLL_MODE, 
                                                         "RF_Discover_Frequency": 2},
                                                        {"RF_Technology_and_Mode":RF_Technology.NFC_F_PASSIVE_POLL_MODE, 
                                                        "RF_Discover_Frequency": 2},
                                                        {"RF_Technology_and_Mode":RF_Technology.NFC_15693_PASSIVE_POLL_MODE, 
                                                        "RF_Discover_Frequency": 2},
                                                        {"RF_Technology_and_Mode":RF_Technology.NFC_A_PASSIVE_LISTEN_MODE, 
                                                         "RF_Discover_Frequency": 2},
                                                        {"RF_Technology_and_Mode":RF_Technology.NFC_F_PASSIVE_LISTEN_MODE, 
                                                        "RF_Discover_Frequency": 2},
                                                        ]}}
