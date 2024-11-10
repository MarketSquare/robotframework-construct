import robotframework_construct
import robotframework_construct.reflector
import pytest
import socket


def test_impossible_params():
    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct()._traverse_construct_for_element(0, 0, 0, 0)
    assert "locator `0´ invalid for `0´" == str(excinfo.value)
    
    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(None, "nope")
    assert "binarydata should be a byte array or a readable binary file object/TCP/UDP socket, but was `<class 'NoneType'>´" == str(excinfo.value)
    
    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(b"", 0)
    assert "identifier should be a string or a construct.Construct, but was `<class 'int'>´" == str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:    
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(0, 0)
    assert "binarydata should be a byte array or a readable binary file object/TCP/UDP socket, but was `<class 'int'>´" == str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().construct_element_should_not_be_equal("a", {"a": [1]}, [1])
    assert "observed value `[1]´ is not distinct to `[1]´ in `{'a': [1]}´ at `a´" == str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().open_socket("raw", 0,0)
    assert "protocol should be either `TCP or `UDP´, but was `raw´" == str(excinfo.value)

def test_tcp_internals():
    r = robotframework_construct.reflector.reflector()
    ps = r.reflector(robotframework_construct.Protocol.TCP)
    for p in ps:
        s1, s2 = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in range(2)]
        with pytest.raises(Exception) as excinfo:
            s1.connect(("127.0.0.1", p))
            s2.connect(("127.0.0.1", p))
    r.shutdown_reflector()
