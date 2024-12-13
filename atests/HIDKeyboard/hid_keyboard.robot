*** Settings ***
Documentation        This is a simple example for a robot file using robotframework-construct demonstrating accessing real HW over the USB HID interface.
...
...                  This currently only tested on linux

Library              robotframework_construct
Library              Dialogs
Variables            hid_keyboard.py
Default Tags         hardware

*** Variables ***
${HID_FILE}           /dev/hidraw0

*** Test Cases ***
Demonstrate USB HID read/write using a USB keyboard as an example
    ${IFILE}=               Open '${HID_FILE}' for reading binary data
    ${OFILE}=               Open '${HID_FILE}' for writing binary data without buffering

    Log to console          ${\n}Press left alt and hold please
    ${LeftAltPressed}=      Parse '${IFILE}' using construct '${HIDReportIn}'
    Element 'modifiers.left_alt' in '${LeftAltPressed}' should be equal to '${True}'
    Log to console          ${\n}Press and hold right shift please
    ${LeftAltPressed}=      Parse '${IFILE}' using construct '${HIDReportIn}'
    Element 'modifiers.right_shift' in '${LeftAltPressed}' should be equal to '${True}'
    Write binary data generated from '${HIDReportOutEmpty}' using construct '${HIDReportOut}' to '${OFILE}'
    Log To Console          ${\n}The three leds should be off now
    Sleep     1
    Modify the element located at 'modifiers.SCROLL_LOCK' of '${HIDReportOutEmpty}' to '${True}'
    Write binary data generated from '${HIDReportOutEmpty}' using construct '${HIDReportOut}' to '${OFILE}'
    Log To Console          ${\n}The scroll lock led should be on now
    Sleep                   time_=1
    Modify the element located at 'modifiers.SCROLL_LOCK' of '${HIDReportOutEmpty}' to '${False}'
    Modify the element located at 'modifiers.CAPS_LOCK' of '${HIDReportOutEmpty}' to '${True}'
    Write binary data generated from '${HIDReportOutEmpty}' using construct '${HIDReportOut}' to '${OFILE}'
    Log To Console          ${\n}The caps lock led should be on now
