*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct using dns as an example for both UDP and TCP.
Variables          dns_construct.py
Library            robotframework_construct
Library            robotframework_construct.reflector
*** Test Cases ***
basic dns request tcp
    ${PORT1}    ${PORT2}=      Reflect traffic between ports using `TCP´
    ${connection1}=   Open TCP connection to server `127.0.0.1´ on port `${PORT1}´
    ${connection2}=   Open TCP connection to server `127.0.0.1´ on port `${PORT2}´
    Write binary data generated from `${exampleRequestRoboconTcp}´ using construct `${dns_payload_tcp}´ to `${connection1}`
    ${record1}=       Parse `${connection2}´ using construct `${dns_payload_tcp}´
    Write binary data generated from `${exampleRequestRoboconTcp}´ using construct `${dns_payload_tcp}´ to `${connection2}`
    ${record2}=       Parse `${connection1}´ using construct `${dns_payload_tcp}´
    Shutdown Reflector

basic dns request udp
    [Tags]    mutation_base
    ${PORT1}    ${PORT2}=      Reflect traffic between ports using `UDP´
    ${connection1}=   Open UDP connection to server `127.0.0.1´ on port `${PORT1}´
    ${connection2}=   Open UDP connection to server `127.0.0.1´ on port `${PORT2}´
    Write binary data generated from `${exampleRequestRoboconUdp}´ using construct `${dns_payload_udp}´ to `${connection1}`
    ${record1}=       Parse `${connection2}´ using construct `${dns_payload_udp}´
    Write binary data generated from `${exampleRequestRoboconUdp}´ using construct `${dns_payload_udp}´ to `${connection2}`
    ${record2}=       Parse `${connection1}´ using construct `${dns_payload_udp}´
    Shutdown Reflector

negative reflect tests
    ${PORT1}    ${PORT2}=           Reflect traffic between ports using `TCP´
    ${connection1}=                 Open TCP connection to server `127.0.0.1´ on port `${PORT1}´
    Run Keyword And Expect Error    *Connection*: * Connection*          Open TCP connection to server `127.0.0.1´ on port `${PORT1}´
