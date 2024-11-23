*** Settings ***
Documentation        This is a simple example for a robot file using robotframework-construct demonstrating accessing real HW (a usb keyboard on linux)
Library              robotframework_construct
Library              Dialogs
Variables            hid_keyboard.py
*** Variables ***
${HID_FILE}           /dev/hidraw0
*** Test Cases ***
Test USB HID keyboard
    ${IFILE}=              Open `${HID_FILE}´ for reading binary data
    ${OFILE}=              Open `${HID_FILE}´ for writing binary data
    Log to console         ${EMPTY}
    Log to console         Press left alt and hold please
    ${LeftAltPressed}=            Parse `${IFILE}´ using construct `${HIDReportIn}´
    Elemement `modifiers.left_alt´ in `${LeftAltPressed}´ should be equal to `${True}´
    Log to console         Press and hold right shift please
    ${LeftAltPressed}=            Parse `${IFILE}´ using construct `${HIDReportIn}´
    Elemement `modifiers.right_shift´ in `${LeftAltPressed}´ should be equal to `${True}´
    Write binary data generated from `${HIDReportOutEmpty}´ using construct `${HIDReportOut}´ to `${OFILE}`
    Call Method   ${OFILE}   flush
    Log To Console         The three leds should be off now
    Sleep     1
    Modify the elemement located at `modifiers.SCROLL_LOCK´ of `${HIDReportOutEmpty}´ to `${True}´
    Write binary data generated from `${HIDReportOutEmpty}´ using construct `${HIDReportOut}´ to `${OFILE}`
    Call Method   ${OFILE}   flush
    Log To Console         The scroll lock led should be on now
    Sleep     1
    Modify the elemement located at `modifiers.SCROLL_LOCK´ of `${HIDReportOutEmpty}´ to `${False}´
    Modify the elemement located at `modifiers.CAPS_LOCK´ of `${HIDReportOutEmpty}´ to `${True}´
    Write binary data generated from `${HIDReportOutEmpty}´ using construct `${HIDReportOut}´ to `${OFILE}`
    Call Method   ${OFILE}   flush
    Log To Console         The caps lock led should be on now
