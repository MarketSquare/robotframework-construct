*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using nfc/nci as an example using UART.
Variables          nci.py
Library            nci
Library            robotframework_construct
Test Teardown      Close NCI Connection
*** Variables ***
${NCI_INTERFACE}    /dev/serial/by-id/usb-STMicroelectronics_STM32_STLink_066EFF3031454D3043225321-if02
${BAUD_RATE}        115200

*** Test Cases ***
#Reset NFC Reseting RF configuration
#    [Documentation]    This test case resets the NFC options using NCI over UART.
#    ${NCI_READ}    ${NCI_WRITE} =    Open NCI Connection Via UART    ${NCI_INTERFACE}    ${BAUD_RATE}
#    Modify the element located at 'payload.ResetType' of '${NFC_RST_CMD}' to '${CORE_RESET_CMD.RESET_CONFIGURATION}'
#    Write Binary Data Generated From '${NFC_RST_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
#    Wait For Data From NCI
#    ${RESET_RESPONSE}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
#    Element 'header.MT' in '${RESET_RESPONSE}' should be equal to '${MessageType.ControlPacketResponse}'
#    Wait For Data From NCI
#    ${RESET_NOTIFICATION}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
#    Element 'header.MT' in '${RESET_NOTIFICATION}' should be equal to '${MessageType.ControlPacketNotification}'
#    Element 'payload.ConfigurationStatus' in '${RESET_NOTIFICATION}' should be equal to '${CONFIGURATION_STATUS.NCI_RF_CONFIGURATION_RESET}'
#
#Reset NFC keeping RF configuration
#    [Documentation]    This test case resets the NFC options using NCI over UART.
#    ${NCI_READ}    ${NCI_WRITE} =    Open NCI Connection Via UART    ${NCI_INTERFACE}    ${BAUD_RATE}
#    
#    Modify the element located at 'payload.ResetType' of '${NFC_RST_CMD}' to '${CORE_RESET_CMD.KEEP_CONFIGURATION}'
#
#    Write Binary Data Generated From '${NFC_RST_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
#    Wait For Data From NCI
#    ${RESET_RESPONSE}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
#    Element 'header.MT' in '${RESET_RESPONSE}' should be equal to '${MessageType.ControlPacketResponse}'
#    Wait For Data From NCI
#    ${RESET_NOTIFICATION}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
#    Element 'header.MT' in '${RESET_NOTIFICATION}' should be equal to '${MessageType.ControlPacketNotification}'
#    Element 'payload.ConfigurationStatus' in '${RESET_NOTIFICATION}' should be equal to '${CONFIGURATION_STATUS.NCI_RF_CONFIGURATION_KEPT}'


Actively poll for A cards
    [Documentation]    This test case resets the NFC options using NCI over UART.
    
    ${NCI_READ}    ${NCI_WRITE} =    Open NCI Connection Via UART    ${NCI_INTERFACE}    ${BAUD_RATE}
    Modify the element located at 'payload.ResetType' of '${NFC_RST_CMD}' to '${CORE_RESET_CMD.RESET_CONFIGURATION}'
    Write Binary Data Generated From '${NFC_RST_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
    Wait For Data From NCI
    Sleep   5
    ${RESET_RESPONSE}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
    Wait For Data From NCI
    ${RESET_RESPONSE}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
    Sleep    0.5
    Write Binary Data Generated From '${NFC_INIT_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
    Wait For Data From NCI
    ${RESET_RESPONSE}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
    Log To Console    ${RESET_RESPONSE}

 


    Write Binary Data Generated From '${NCI_DISCVER_CMD}' Using Construct '${NCIControlPacket}' To '${NCI_WRITE}'
    Wait For Data From NCI
    ${RESET_RESPONSE}=     Parse '${NCI_READ}' Using Construct '${NCIControlPacket}'
    Log To Console    ${RESET_RESPONSE}
    Sleep    0.5
