*** Settings ***
Documentation      This are tests checking for sensible error messages.
...
...                This is usefull for quality controll and for trouble shooting. These examples might help to understand the error messages.
Library            bson            
Library            robotframework_construct
Test Tags         mutation_base
*** Test Cases ***
simple negative tests
    Register construct 'document' from 'bson_construct' as 'bson_document'
    ${my_dict}=         Create Dictionary    hey=you    number=${1}
    ${blob}=            bson.encode       ${my_dict}
    ${returnedDict}=         Parse '${blob}' using construct 'bson_document'

    Run keyword and expect error       could not find construct '0'                                                                    Parse '${blob}' using construct '${0}'
    Run keyword and expect error       observed value '1' does not match expected '0' in 'Container:*                                  Element 'elements.1.value' in '${returnedDict}' should be equal to '0'
    Run keyword and expect error       observed value '1' does not match expected '2' in 'Container:*                                  Element 'elements.1.value' in '${returnedDict}' should be equal to '2'
    Run keyword and expect error       could not find 'elements.1.nope' in 'Container:*'                                               Element 'elements.1.nope' in '${returnedDict}' should be equal to '1'
    Run keyword and expect error       locator 'elements.nope.value' invalid for 'Container:*'                                         Element 'elements.nope.value' in '${returnedDict}' should be equal to '1'
    Run keyword and expect error       locator 'elements.-1.value' invalid for 'Container:*'                                           Element 'elements.-1.value' in '${returnedDict}' should be equal to '1'
    Run keyword and expect error       could not convert 'nope' of type '<class 'str'>' to '<class 'int'>' of the original value '1'   Element 'elements.1.value' in '${returnedDict}' should be equal to 'nope'
    Run keyword and expect error       could not find 'elements.1.nope' in 'Container:*                                                Modify the element located at 'elements.1.nope' of '${returnedDict}' to '0'
    Run keyword and expect error       could not convert 'nope' of type '<class 'str'>' to '<class 'int'>' of the original value '1'   Modify the element located at 'elements.1.value' of '${returnedDict}' to 'nope'
    Run keyword and expect error       locator 'elements.-1.value' invalid for 'Container:*'                                           Modify the element located at 'elements.-1.value' of '${returnedDict}' to '0'
    Run keyword and expect error       locator 'elements.nope.value' invalid for 'Container:*'                                         Modify the element located at 'elements.nope.value' of '${returnedDict}' to '0'
    Run keyword and expect error       observed value '1' does not match expected '2' in 'Container:*                                  Element 'elements.1.value' in '${returnedDict}' should be equal to '2'
    Run keyword and expect error       observed value '1' does not match expected '4' in 'Container:*                                  Element 'elements.1.value' in '${returnedDict}' should be equal to '4'