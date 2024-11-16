*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using bson as an example. 
...                To run it use.:
...                uv run robot -P examples/bson/ examples/bson/simple_bson.robot
Library            bson            
Library            robotframework_construct
Test Tags          mutation_base
*** Test Cases ***
    
Simple positive element checks
    Register construct `document´ from `bson_construct´ as `bson_document´
    ${my_dict}=         Create Dictionary    hey=you    number=${1}
    ${blob}=            bson.encode       ${my_dict}
    ${returnedDict}=    Parse `${blob}´ using construct `bson_document´
    Elemement `elements.1.value´ in `${returnedDict}´ should be equal to `1´
    Elemement `elements.1.value´ in `${returnedDict}´ should not be equal to `0´
    Elemement `elements.1.value´ in `${returnedDict}´ should not be equal to `2´
    Elemement `elements.0.value´ in `${returnedDict}´ should be equal to `you´
    Elemement `elements.0.value´ in `${returnedDict}´ should not be equal to `me´
    ${blob2}=           Generate binary from `${returnedDict}´ using construct `bson_document´
    Should Be Equal     ${blob}    ${blob2}
    Modify the elemement located at `elements.1.value´ of `${returnedDict}´ to `${3}´
    Elemement `elements.1.value´ in `${returnedDict}´ should be equal to `3´
    Elemement `elements.1.value´ in `${returnedDict}´ should not be equal to `2´
    Elemement `elements.1.value´ in `${returnedDict}´ should not be equal to `4´
    Set element seperator to `->´
    Elemement `elements->1->value´ in `${returnedDict}´ should be equal to `3´
    Elemement `elements->1->value´ in `${returnedDict}´ should not be equal to `2´
    Elemement `elements->1->value´ in `${returnedDict}´ should not be equal to `4´
    Set element seperator to `.´

simple positive element checks using a file
    Register construct `document´ from `bson_construct´ as `bson_document´
    ${my_dict}=         Create Dictionary    hey=you    number=${1}
    ${blob}=            bson.encode       ${my_dict}
    ${my_dict}=         Parse `${blob}´ using construct `bson_document´
    ${my_dict}=         Evaluate    {'size': 30, 'elements': ([dict(type=2, name=u'hey', value=u'you'), dict(type=16, name=u'number', value=1)])}
    ${OFILE}=           Open `temp_binary.blob´ for writing binary data
    Write binary data generated from `${my_dict}´ using construct `bson_document´ to `${OFILE}`
    Call Method         ${OFILE}    flush
    ${IFILE}=           Open `temp_binary.blob´ for reading binary data
    ${my_dict2}=        Parse `${IFILE}´ using construct `bson_document´
    ${blob2}=           Generate binary from `${my_dict2}´ using construct `bson_document´
    Should Be Equal     ${blob}    ${blob2}
