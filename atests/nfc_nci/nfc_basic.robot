*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using nfc/nci as an example using UART.
Variables          nci.py
Library            nci_interface
Library            nci
Library            robotframework_construct
Test Teardown      Close NCI Connection
Default Tags       hardware
*** Variables ***
${NCI_INTERFACE}    /dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_066EFF3031454D3043225321-if02
${BAUD_RATE}        115200

*** Test Cases ***
Reset NFC Reseting RF configuration
    [Documentation]    This test case resets the NFC options using NCI over UART reseting the RF configuration.
    ${NCI_READ}    ${NCI_WRITE} =    Open NCI Connection Via UART    ${NCI_INTERFACE}    ${BAUD_RATE}
    Sleep    0.25
    Empty Nci Connection Receive Buffer
    Modify the element located at 'payload.ResetType' of '${NFC_RST_CMD}' to '${CORE_RESET_CMD.RESET_CONFIGURATION}'
    Write Binary Data Generated From '${NFC_RST_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
    Expect Response from ${NCI_READ} of type ${MT.ControlPacketResponse}
    ${RESET_NOTIFICATION}=    Expect Response from ${NCI_READ} of type ${MT.ControlPacketNotification}
    Element 'payload.ConfigurationStatus' in '${RESET_NOTIFICATION}' should be equal to '${CONFIGURATION_STATUS.NCI_RF_CONFIGURATION_RESET}'
    Nci Connection Receive Buffer Should Be Empty

Reset NFC keeping RF configuration
    [Documentation]    This test case resets the NFC options using NCI over UART keeping the RF configuration.
    ${NCI_READ}    ${NCI_WRITE} =    Open NCI Connection Via UART    ${NCI_INTERFACE}    ${BAUD_RATE}
    Sleep    0.25
    Empty Nci Connection Receive Buffer
    Modify the element located at 'payload.ResetType' of '${NFC_RST_CMD}' to '${CORE_RESET_CMD.KEEP_CONFIGURATION}'
    Write Binary Data Generated From '${NFC_RST_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
    Expect Response from ${NCI_READ} of type ${MT.ControlPacketResponse}
    ${RESET_NOTIFICATION}=    Expect Response from ${NCI_READ} of type ${MT.ControlPacketNotification}
    Element 'payload.ConfigurationStatus' in '${RESET_NOTIFICATION}' should be equal to '${CONFIGURATION_STATUS.NCI_RF_CONFIGURATION_KEPT}'
    Nci Connection Receive Buffer Should Be Empty

Actively poll for A cards
    [Documentation]    This test case resets the NFC options using NCI over UART.
    ${NCI_READ}    ${NCI_WRITE} =    Open NCI Connection Via UART    ${NCI_INTERFACE}    ${BAUD_RATE}
    Sleep    0.25
    Empty Nci Connection Receive Buffer
    Write Binary Data Generated From '${NFC_RST_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
    Expect Response from ${NCI_READ} of type ${MT.ControlPacketResponse}
    Expect Response from ${NCI_READ} of type ${MT.ControlPacketNotification}
    Write Binary Data Generated From '${NFC_INIT_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
    Expect Status OK response from ${NCI_READ}
    Write Binary Data Generated From '${NCI_DISCVER_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
    Expect Status OK response from ${NCI_READ}
    Log to console            please place a card on the reader
    Wait For Data From NCI    timeout=1
    ${RESPONSE}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
    Wait For Data From NCI    timeout=1
    ${RESPONSE}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'

*** Keywords ***
Receive message from NCI from ${NCI_READ}
    Wait For Data From NCI
    ${RESPONSE}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
    RETURN    ${RESPONSE}

Expect Status OK response from ${NCI_READ}
    ${RESPONSE}=      Receive message from NCI from ${NCI_READ}
    Element 'payload.Status' in '${RESPONSE}' should be equal to '${GENERIC_STATUS_CODE.STATUS_OK}'
    RETURN    ${RESPONSE}

Expect Response from ${NCI_READ} of type ${EXPECTED_MT}
    ${RESPONSE}=     Receive message from NCI from ${NCI_READ}
    Element 'header.MT' in '${RESPONSE}' should be equal to '${EXPECTED_MT}'
    RETURN    ${RESPONSE}

