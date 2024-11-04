*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using bson as an example. 
...                To run it use.:
...                uv run robot -P examples/bson/ examples/bson/simple_bson.robot
Library            bson            
Library            robotframework_construct
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