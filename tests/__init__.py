import os
import robotframework_construct
import robot.api.logger
import pytest


def test_impossible_params():
    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct()._traverse_construct_for_element(0, 0, 0, 0)
    assert "locator '0' invalid for '0'" == str(excinfo.value)
    
    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(None, "nope")
    assert "binarydata should be a byte array or a readable binary file object/TCP/UDP socket, but was '<class 'NoneType'>'" == str(excinfo.value)
    
    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(b"", 0)
    assert "identifier should be a string or a construct.Construct, but was '<class 'int'>'" == str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:    
        robotframework_construct.robotframework_construct().parse_binary_data_using_construct(0, 0)
    assert "binarydata should be a byte array or a readable binary file object/TCP/UDP socket, but was '<class 'int'>'" == str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().construct_element_should_not_be_equal("a", {"a": [1]}, [1])
    assert "observed value '[1]' is not distinct to '[1]' in '{'a': [1]}' at 'a'" == str(excinfo.value)

    with pytest.raises(AssertionError) as excinfo:
        robotframework_construct.robotframework_construct().open_socket("raw", 0,0)
    assert "protocol should be either 'TCP or 'UDP', but was 'raw'" == str(excinfo.value)

loggerInput = None

@pytest.fixture
def mock_logger(monkeypatch):
    def logger(message):
        global loggerInput
        loggerInput = message

    monkeypatch.setattr(robot.api.logger, "info", logger)

def test_logging_feature_with_hex_output(mock_logger):
    rc = robotframework_construct.robotframework_construct()
    rc._log_generated_bytes(1, b"", {a: a for a in range(12)})
    assert os.linesep not in loggerInput

def test_logging_feature_with_hex_output_Extra_newline(mock_logger):
    rc = robotframework_construct.robotframework_construct()
    rc._log_generated_bytes(1, b"", {a: a for a in range(13)})
    assert os.linesep in loggerInput
    assert f'''" from :"{os.linesep}'''

def test_logging_feature_with_long_buf(mock_logger):
    rc = robotframework_construct.robotframework_construct()
    binBuf = b"\x01" * 65
    rc._log_generated_bytes(1, binBuf, 1)
    assert "01 "*64 in loggerInput
    assert "01 "*65 not in loggerInput
