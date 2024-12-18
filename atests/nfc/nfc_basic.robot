*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using nfc/nfc as an example using UART.
Variables          nfc.py
Library            nfc_interface
Library            robotframework_construct
Test Teardown      Close nfc Connection
Default Tags       hardware
*** Variables ***
${NFC_INTERFACE}    /dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_066EFF3031454D3043225321-if02
${BAUD_RATE}        115200

*** Test Cases ***
Reset NFC Reseting RF configuration
    [Documentation]    This test case resets the NFC options using nfc over UART reseting the RF configuration.
    ${NFC_INTERFACE}=    Open nfc Connection Via UART    ${NFC_INTERFACE}    ${BAUD_RATE}
    Sleep    0.25
    Empty nfc Connection Receive Buffer
    Modify the element located at 'payload.ResetType' of '${NFC_RST_CMD}' to '${CORE_RESET_CMD.RESET_CONFIGURATION}'
    Write Binary Data Generated From '${NFC_RST_CMD}' Using Construct '${nfcControlPacket}' To '${NFC_INTERFACE}'
    Expect Response from ${NFC_INTERFACE} of type ${MT.ControlPacketResponse}
    ${RESET_NOTIFICATION}=    Expect Response from ${NFC_INTERFACE} of type ${MT.ControlPacketNotification}
    Element 'payload.ConfigurationStatus' in '${RESET_NOTIFICATION}' should be equal to '${CONFIGURATION_STATUS.NFC_RF_CONFIGURATION_RESET}'
    NFC Connection Receive Buffer Should Be Empty

Reset NFC keeping RF configuration
    [Documentation]    This test case resets the NFC options using nfc over UART keeping the RF configuration.
    ${NFC_INTERFACE} =    Open nfc Connection Via UART    ${NFC_INTERFACE}    ${BAUD_RATE}
    Sleep    0.25
    Empty NFC Connection Receive Buffer
    Modify the element located at 'payload.ResetType' of '${NFC_RST_CMD}' to '${CORE_RESET_CMD.KEEP_CONFIGURATION}'
    Write Binary Data Generated From '${NFC_RST_CMD}' Using Construct '${nfcControlPacket}' To '${NFC_INTERFACE}'
    Expect Response from ${NFC_INTERFACE} of type ${MT.ControlPacketResponse}
    ${RESET_NOTIFICATION}=    Expect Response from ${NFC_INTERFACE} of type ${MT.ControlPacketNotification}
    Element 'payload.ConfigurationStatus' in '${RESET_NOTIFICATION}' should be equal to '${CONFIGURATION_STATUS.NFC_RF_CONFIGURATION_KEPT}'
    NFC Connection Receive Buffer Should Be Empty

Actively poll for A cards
    [Documentation]    This test case resets the NFC options using nfc over UART.
    ${NFC_INTERFACE}=    Open NFC Connection Via UART    ${NFC_INTERFACE}    ${BAUD_RATE}
    Sleep    0.25
    Empty NFC Connection Receive Buffer
    Write Binary Data Generated From '${NFC_RST_CMD}' Using Construct '${nfcControlPacket}' To '${NFC_INTERFACE}'
    Expect Response from ${NFC_INTERFACE} of type ${MT.ControlPacketResponse}
    Expect Response from ${NFC_INTERFACE} of type ${MT.ControlPacketNotification}
    Write Binary Data Generated From '${NFC_INIT_CMD}' Using Construct '${nfcControlPacket}' To '${NFC_INTERFACE}'
    Expect Status OK response from ${NFC_INTERFACE}
    Write Binary Data Generated From '${NFC_DISCVER_CMD}' Using Construct '${NFCControlPacket}' To '${NFC_INTERFACE}'
    Expect Status OK response from ${NFC_INTERFACE}
    Log to console            please place a card on the reader
    Wait For Data From NFC    timeout=1
    ${RESPONSE}=     Parse '${NFC_INTERFACE}' Using Construct '${NFCControlPacket}'
    Wait For Data From NFC    timeout=1
    ${RESPONSE}=     Parse '${NFC_INTERFACE}' Using Construct '${nfcControlPacket}'

*** Keywords ***
Receive message from nfc from ${nfc_INTERFACE}
    Wait For Data From nfc
    ${RESPONSE}=     Parse '${nfc_INTERFACE}' Using Construct '${nfcControlPacket}'
    RETURN    ${RESPONSE}

Expect Status OK response from ${nfc_INTERFACE}
    ${RESPONSE}=      Receive message from nfc from ${nfc_INTERFACE}
    Element 'payload.Status' in '${RESPONSE}' should be equal to '${GENERIC_STATUS_CODE.STATUS_OK}'
    RETURN    ${RESPONSE}

Expect Response from ${nfc_INTERFACE} of type ${EXPECTED_MT}
    ${RESPONSE}=     Receive message from nfc from ${nfc_INTERFACE}
    Element 'header.MT' in '${RESPONSE}' should be equal to '${EXPECTED_MT}'
    RETURN    ${RESPONSE}

