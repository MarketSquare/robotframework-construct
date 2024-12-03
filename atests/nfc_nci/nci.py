from construct import Struct, Int8ub, Bytes, BitStruct, BitsInteger, this, Byte, Enum, Switch, Const, Array, Int16ub, If


MessageType = Enum(BitsInteger(3),
    DATA=0,
    ControlPacketCommand=1,
    ControlPacketResponse=2,
    ControlPacketNotification=3)

PacketBoundaryFlag = Enum(BitsInteger(1),
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

CONFIGURATION_STATUS = Enum(Byte,NCI_RF_CONFIGURATION_KEPT=0,NCI_RF_CONFIGURATION_RESET=1) # Table 7
NCI_VERSION = Enum(Byte,NCI_VERSION_1_0=0x10,NCI_VERSION_2_0=0x20) # Table 6 
CORE_RESET_NTF_STATUS_REASON_CODE = Enum(Byte, UNSPECIFIED=0x00, CORE_RESET_TRIGGERED=0x01)

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


CORE_INIT_RSP_PAYLOAD = Struct("Status"                           / CORE_RESET_RSP_STATUS,
                               "NFCC_Features"                    / NFCC_FEATURES,
                               "NumInterfaces"                    / Byte,
                               "SupportedInterfaces"              / Array(this.NumInterfaces, RF_INTERFACES),
                               "Max_Logical_Connections"          / Int8ub,
                               "Max_Routing_Table_Size"           / Int16ub,
                               "Max_Control_Package_Payload_Size" / Int8ub,
                               "Max_Size_for_Large_Parameters"    / Int8ub)

CORE_RESET_RSP = Struct("Status"               / If(this._.payload_length>=1, CORE_RESET_RSP_STATUS),
                        "NCI_Version"          / If(this._.payload_length>=2            , NCI_VERSION),
                        "ConfigurationStatus"  / If(this._.payload_length>=3, CONFIGURATION_STATUS),
                        "padding"              / If(this._.payload_length>3, Bytes(max(0, this._.payload_length-3))))

CORE_RESET_NTF = Struct("Reason"              / CORE_RESET_NTF_STATUS_REASON_CODE,
                        "ConfigurationStatus" / CONFIGURATION_STATUS)

NCIDataPacket = Struct(
    "header"            / BitStruct(
        "MT"            / MessageType,
        "PBF"           / PacketBoundaryFlag,
        "ConnID"        / BitsInteger(4),
        "RFU"           / Byte,  
        "PayloadLength" / Byte
    ),
    "payload_length" / Int8ub,
    "payload" / Bytes(this.payload_length)
)

CORE_RESET_CMD_PAYLOAD = Struct("ResetType" / CORE_RESET_CMD)

NCIControlPacket = Struct(
    "header" / BitStruct("MT" / MessageType,
                         "PBF" / PacketBoundaryFlag,
                         "GID" / GID,
                         "RFU" / BitsInteger(2),
                         "OID" / Switch(this.GID, {GID.CORE: OID_NCI_Core, GID.RF: OID_RF_Management, GID.NFCEE: OID_NFCEE_Management})),
    "payload_length" / Int8ub,
    "payload" / Switch((this.header.MT, this.header.GID, this.header.OID,), {(MessageType.ControlPacketCommand,      GID.CORE, OID_NCI_Core.CORE_RESET,):       CORE_RESET_CMD_PAYLOAD,
                                                                             (MessageType.ControlPacketResponse,     GID.CORE, OID_NCI_Core.CORE_RESET,):       CORE_RESET_RSP,
                                                                             (MessageType.ControlPacketNotification, GID.CORE, OID_NCI_Core.CORE_RESET,):       CORE_RESET_NTF,
                                                                             (MessageType.ControlPacketCommand,      GID.CORE, OID_NCI_Core.CORE_INIT,):        Const(b""),
                                                                             (MessageType.ControlPacketResponse,     GID.CORE, OID_NCI_Core.CORE_INIT,):        CORE_INIT_RSP_PAYLOAD,
                                                                             }))
