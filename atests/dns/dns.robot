*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using dns as an example for both UDP and TCP.
Variables          dns_construct.py
Library            robotframework_construct
*** Test Cases ***
basic dns request tcp
    ${connection}=   Open TCP connection to server `1.1.1.1´ on port `53´
    Write binary data generated from `${exampleRequestRoboconTcp}´ using construct `${dns_payload_tcp}´ to `${connection}`
    ${record}=       Parse `${connection}´ using construct `${dns_payload_tcp}´
    Check dns response `${record}´ against hostname `robocon.io´

basic dns request udp
    ${connection}=   Open UDP connection to server `1.1.1.1´ on port `53´
    Write binary data generated from `${exampleRequestRoboconUdp}´ using construct `${dns_payload_udp}´ to `${connection}`
    ${record}=       Parse `${connection}´ using construct `${dns_payload_udp}´
    Check dns response `${record}´ against hostname `robocon.io´
    
*** Keywords ***
Check dns response `${record}´ against hostname `${hostname}´
    ${NrResponses}=         Get elemement `ancount´ from `${record}´
    ${ip}=                  Evaluate    [int(item) for item in socket.gethostbyname('${hostname}').split(".")]    modules=socket
    FOR   ${idx}    IN RANGE    ${NrResponses}
        ${passed}=          Run Keyword And Return Status	Check dns response `${record}´ answer number `${idx}´ ip adress `${ip}´
        Run keyword if      ${passed}                       Return from keyword
    END
    Fail    Ip adress not found in dns response

Check dns response `${record}´ answer number `${idx}´ ip adress `${ip}´
    FOR  ${i}    IN RANGE     ${4}
        Elemement `answers.${idx}.rdata.${i}´ in `${record}´ should be equal to `${ip}[${i}]´
    END