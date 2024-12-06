import os
from construct import Struct, Byte, Array, BitStruct, Flag, Enum, Padding


_ModifierBitfield = BitStruct(
    "SCROLL_LOCK" / Flag,  # Bit 0
    "NUM_LOCK" / Flag,     # Bit 1
    "CAPS_LOCK" / Flag,    # Bit 2
    Padding(5),            # Bits 3–7 (reserved)
)


_KeycodeEnum = Enum(
    Byte,
    A=0x04,
    B=0x05,
    C=0x06,
    D=0x07,
    E=0x08,
    F=0x09,
    G=0x0A,
    H=0x0B,
    I=0x0C,
    J=0x0D,
    K=0x0E,
    L=0x0F,
    M=0x10,
    N=0x11,
    O=0x12,
    P=0x13,
    Q=0x14,
    R=0x15,
    S=0x16,
    T=0x17,
    U=0x18,
    V=0x19,
    W=0x1A,
    X=0x1B,
    Y=0x1C,
    Z=0x1D,
    _1=0x1E,
    _2=0x1F,
    _3=0x20,
    _4=0x21,
    _5=0x22,
    _6=0x23,
    _7=0x24,
    _8=0x25,
    _9=0x26,
    _0=0x27,
    ENTER=0x28,
    ESC=0x29,
    BACKSPACE=0x2A,
    TAB=0x2B,
    SPACE=0x2C,
    CAPS_LOCK=0x39,
)

HIDReportIn = Struct(
    "modifiers" / BitStruct("right_gui"     / Flag,
                            "right_alt"     / Flag,
                            "right_shift"   / Flag,
                            "right_ctrl"    / Flag,
                            "left_gui"      / Flag,
                            "left_alt"      / Flag,
                            "left_shift"    / Flag,
                            "left_ctrl"     / Flag,
                            ),
    "reserved" / Byte,  
    "keys" / Array(6, _KeycodeEnum)
)
HIDReportIn.name = "HIDReportIn"

HIDReportOut = Struct("ReportID" / Byte,
                      "modifiers" / BitStruct(Padding(5),
                                              "SCROLL_LOCK" / Flag,
                                              "NUM_LOCK"    / Flag,
                                              "CAPS_LOCK"   / Flag,
                                              ),
                      "reserved"  / Array(6, Byte)
)
HIDReportOut.name = "HIDReportOut"

HIDReportOutEmpty = {"ReportID": 0, "modifiers": {"SCROLL_LOCK": False, "NUM_LOCK": False, "CAPS_LOCK": False}, "reserved": [0,0,0,0,0,0]}
