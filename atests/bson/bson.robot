*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using the bson file format as an example, loading the constructs from a python module.
Library            bson            
Library            robotframework_construct
Test Tags          mutation_base
Test Setup         Setup BSON

*** Keywords ***
Setup BSON
    Register construct 'document' from 'bson_construct' as 'bson_document'
    ${my_dict}         Create Dictionary    hey=you    number=${1}
    ${blob}            bson.encode       ${my_dict}
    Set Test Variable  ${blob}
    Set Test Variable  ${my_dict}

*** Test Cases ***
simple bson example using a in memory object
    ${returnedDict}=    Parse '${blob}' using construct 'bson_document'
    ${element}=         Get element 'elements.1.value' from '${returnedDict}'
    Should Be Equal As Integers    ${element}    1
    Element 'elements.1.value' in '${returnedDict}' should be equal to '1'
    Element 'elements.1.value' in '${returnedDict}' should not be equal to '0'
    Element 'elements.1.value' in '${returnedDict}' should not be equal to '2'
    Element 'elements.0.value' in '${returnedDict}' should be equal to 'you'
    Element 'elements.0.value' in '${returnedDict}' should not be equal to 'me'

simple roundtrip parse/generate example using bson
    ${returnedDict}=    Parse '${blob}' using construct 'bson_document'
    ${blob2}=           Generate binary from '${returnedDict}' using construct 'bson_document'
    Should Be Equal     ${blob}    ${blob2}

simple bson example using a in memory object including modification
    ${returnedDict}=    Parse '${blob}' using construct 'bson_document'
    Modify the element located at 'elements.1.value' of '${returnedDict}' to '${3}'
    Element 'elements.1.value' in '${returnedDict}' should be equal to '3'
    Element 'elements.1.value' in '${returnedDict}' should not be equal to '2'
    Element 'elements.1.value' in '${returnedDict}' should not be equal to '4'

simple bson example changint the seperator
    ${returnedDict}=    Parse '${blob}' using construct 'bson_document'
    Set element seperator to '->'
    Element 'elements->1->value' in '${returnedDict}' should be equal to '1'
    Set element seperator to '.'

simple bson example using a file with buffering
    Register construct 'document' from 'bson_construct' as 'bson_document'
    ${my_dict}=         Create Dictionary    hey=you    number=${1}
    ${blob}=            bson.encode       ${my_dict}
    ${my_dict}=         Parse '${blob}' using construct 'bson_document'
    ${my_dict}=         Evaluate    {'size': 30, 'elements': ([dict(type=2, name=u'hey', value=u'you'), dict(type=16, name=u'number', value=1)])}
    ${OFILE}=           Open 'temp_binary.blob' for writing binary data
    Write binary data generated from '${my_dict}' using construct 'bson_document' to '${OFILE}'
    Call Method         ${OFILE}    flush
    ${IFILE}=           Open 'temp_binary.blob' for reading binary data
    ${my_dict2}=        Parse '${IFILE}' using construct 'bson_document'
    ${blob2}=           Generate binary from '${my_dict2}' using construct 'bson_document'
    Should Be Equal     ${blob}    ${blob2}

simple bson example using a file without buffering
    Register construct 'document' from 'bson_construct' as 'bson_document'
    ${my_dict}=         Create Dictionary    hey=you    number=${1}
    ${blob}=            bson.encode       ${my_dict}
    ${my_dict}=         Parse '${blob}' using construct 'bson_document'
    ${my_dict}=         Evaluate    {'size': 30, 'elements': ([dict(type=2, name=u'hey', value=u'you'), dict(type=16, name=u'number', value=1)])}
    ${OFILE}=           Open 'temp_binary.blob' for writing binary data without buffering
    Write binary data generated from '${my_dict}' using construct 'bson_document' to '${OFILE}'
    ${IFILE}=           Open 'temp_binary.blob' for reading binary data
    ${my_dict2}=        Parse '${IFILE}' using construct 'bson_document'
    ${blob2}=           Generate binary from '${my_dict2}' using construct 'bson_document'
    Should Be Equal     ${blob}    ${blob2}
