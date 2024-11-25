import robot.api
import construct
import io
import importlib
import re
from robot.api.deco import keyword
import robot.api.logger
import socket
import pathlib
import enum
import typing


_port_mapping = {}

_U = typing.TypeVar("_U")


class Protocol(enum.Enum):
    TCP = "TCP"
    UDP = "UDP"


class _construct_interface_basics:
    def __init__(self, element_seperator: str =r".") -> None:
        self.set_element_seperator(element_seperator)

    def _convert_to_current_type(self, expectedValue: _U, element: typing.Any) -> _U:
        try:
            expectedValue = type(element)(expectedValue)
        except ValueError:
            assert False, f"could not convert `{expectedValue}´ of type `{type(expectedValue)}´ to `{type(element)}´ of the original value `{element}´"
        return expectedValue

    def _get_element_from_constructDict(self, constructDict: typing.Union[dict, construct.Struct], locator: str) -> typing.Union[dict, construct.Struct]:
        assert isinstance(constructDict, dict), f"constructDict should be a dict, but was `{type(constructDict)}´"
        assert isinstance(locator, str), f"locator should be a string, but was `{type(locator)}´"
        original = constructDict
        try:
            for item in self._split_at_dot_escape_with_dotdot.split(locator):
                constructDict = self._traverse_construct_for_element(constructDict, locator, original, item)
        except (KeyError, TypeError, IndexError):
            assert False, f"could not find `{locator}´ in `{original}´"
        return constructDict

    def _set_element_from_constructDict(self, constructDict: typing.Union[dict, construct.Struct], locator: str, value) -> None:
        assert isinstance(constructDict, dict), f"constructDict should be a dict, but was `{type(constructDict)}´"
        assert isinstance(locator, str), f"locator should be a string, but was `{type(locator)}´"
        original = constructDict
        try:
            element_chain = self._split_at_dot_escape_with_dotdot.split(locator)
            target = element_chain[-1]
            element_chain = element_chain[:-1]
            for item in element_chain:
                constructDict = self._traverse_construct_for_element(constructDict, locator, original, item)
            orig = constructDict[target]
        except (IndexError, KeyError):
            assert False, f"could not find `{locator}´ in `{original}´"
        try:
            value = type(orig)(value)
        except ValueError:
            assert False, f"could not convert `{value}´ of type `{type(value)}´ to `{type(orig)}´ of the original value `{orig}´"
        constructDict[target] = value

    def _traverse_construct_for_element(self, constructDict: typing.Union[dict, construct.Struct], locator: str, original: typing.Union[dict, construct.Struct], item: str) -> typing.Union[dict, construct.Struct]:
        robot.api.logger.info(f"descending to `{item}´ of `{constructDict}´")
        match (item, constructDict,):
            case (str(), dict(),):
                constructDict = constructDict[item]
            case (str(y), list(),) if all(x.isdigit() for x in y):  
                constructDict = constructDict[int(item)]
            case _:
                assert False, f"locator `{locator}´ invalid for `{original}´"
        return constructDict

    @keyword('Set element seperator to `${element_seperator}´')
    def set_element_seperator(self, element_seperator: str) -> None:
        """Sets the element seperator to element_seperator.

        Arguments:
        | =Arguments=     | =Description= |
        | element_seperator | The seperator to be used for element location, by default it is ".", other popular choices are "->". |
        """
        element_seperator = re.escape(element_seperator)
        self._split_at_dot_escape_with_dotdot = re.compile(rf'(?<!{element_seperator}){element_seperator}(?!{element_seperator})')

    @keyword('Elemement `${locator}´ in `${constructDict}´ should be equal to `${expectedValue}´')
    def construct_element_should_be_equal(self, locator:str, constructDict: typing.Union[dict, construct.Struct], expectedValue) -> None:
        """Checks that the element located at locator in construct is equal to expectedValue.

        Arguments:
        | =Arguments=   | =Description= |
        | locator       | The location of the element to be checked |
        | constructDict | The dictionary/list to be checked, intended to be used for construct |
        | expectedValue | The value the element should be equal to |

        The locator is a name/index series seperated by the seperator. The seperator can be set with `Set element seperator to´, by default it is ".".
        """
        element = self._get_element_from_constructDict(constructDict, locator)
        expectedValue = self._convert_to_current_type(expectedValue, element)
        assert element == expectedValue, f"observed value `{str(element)}´ does not match expected `{expectedValue}´ in `{str(constructDict)}´ at `{locator}´"

    @keyword('Elemement `${locator}´ in `${constructDict}´ should not be equal to `${expectedValue}´')
    def construct_element_should_not_be_equal(self, locator:str, constructDict: typing.Union[dict, construct.Struct], expectedValue) -> None:
        """Checks that the element located at locator in construct is _not_ equal to expectedValue.

        Arguments:
        | =Arguments=   | =Description= |
        | locator       | The location of the element to be checked |
        | constructDict | The dictionary/list to be checked, intended to be used for construct |
        | expectedValue | The value the element should be equal to |

        The locator is a name/index series seperated by the seperator. The seperator can be set with `Set element seperator to´, by default it is ".".
        """
        element = self._get_element_from_constructDict(constructDict, locator)
        expectedValue = self._convert_to_current_type(expectedValue, element)
        assert element != expectedValue, f"observed value `{str(element)}´ is not distinct to `{expectedValue}´ in `{str(constructDict)}´ at `{locator}´"

    @keyword('Get elemement `${locator}´ from `${constructDict}´')
    def get_construct_element(self, locator:str, constructDict: typing.Union[dict, construct.Struct]) -> typing.Union[dict, construct.Struct]:
        """Retreives the element located at locator in constructDict.

        Arguments:
        | =Arguments=   | =Description= |
        | locator       | The location of the element to be retreived |
        | constructDict | The dictionary/list to be checked, intended to be used for construct |

        The locator is a name/index series seperated by the seperator. The seperator can be set with `Set element seperator to´, by default it is ".".
        """
        return self._get_element_from_constructDict(constructDict, locator)

    @keyword('Modify the elemement located at `${locator}´ of `${constructDict}´ to `${value}´')
    def set_construct_element(self, locator:str, constructDict: typing.Union[dict, construct.Struct], value) -> typing.Union[dict, construct.Struct]:
        """Modifies the element located at locator in constructDict to the value value.

        Arguments:
        | =Arguments=   | =Description= |
        | locator       | The location of the element to be retreived |
        | constructDict | The dictionary/list to be checked, intended to be used for construct |
        | value         | The value to be assigned to the location |

        The locator is a name/index series seperated by the seperator. The seperator can be set with `Set element seperator to´, by default it is ".".
        """
        self._set_element_from_constructDict(constructDict, locator, value)
        return constructDict


class robotframework_construct(_construct_interface_basics):
    """Library for parsing and generating binary data beatifuly using the `construct´ library.

    This is the keyword documentation for robotframework-construct library. For information
    about installation, support, and more please visit the
    [https://github.com/MarketSquare/robotframework-construct].
    For more information about Robot Framework itself, see [https://robotframework.org|robotframework.org].

    robotframework-construct uses [https://construct.readthedocs.io/en/latest/|construct] to parse and generate binary data.

    Use cases

    - Register map access and visualization
    - I2C/SPI/UART/CAN communication
    - Binary network protocol (TCP/UDP), binary file, and memory object handling

    """
    def __init__(self):
        self.constructs = {}
        super().__init__()

    @keyword('Register construct `${spec}´ from `${library}´ as `${identifier}´')
    def register_construct(self, spec: str, library: str, identifier: str) -> None:
        """Makes a construct available for parsing and generating binary data. This construct 
        may be a regular construct, which is residing in a module, just like regular constructs do.

        Arguments:
        | =Arguments= | =Description= |
        | spec        | The name of the construct to be registered |
        | library     | The name of the library this construct resides in |
        | identifier  | The name which will be available to adress this construct |

        This allows to use a construct from a preexisiting library without any cooperation from this library.
        """
        lib = importlib.import_module(library)
        spec = getattr(lib, spec)
        assert isinstance(spec, construct.Construct), f"spec should be a construct.Construct, but was `{type(spec)}´"
        self.constructs[identifier] = spec

    @keyword('Parse `${binarydata}´ using construct `${identifier}´')
    def parse_binary_data_using_construct(self, binarydata: bytes|io.IOBase|socket.socket, identifier: typing.Union[str, construct.Construct]) -> construct.Struct:
        """Parses binary data using a construct. The binary data can be a byte array, a readable binary file object, or a TCP/UDP socket.

        Arguments:
        | =Arguments= | =Description= |
        | binarydata  | The binary data to be parsed (bytes, binary file object or TCP/UDP socket) |
        | identifier  | The construct to be used for parsing, either as registered with 'Register construct' or a construct type variable |

        """
        match binarydata:
            case socket.socket():
                binarydata = binarydata.makefile("rb")
            case bytes():
                binarydata = io.BytesIO(binarydata)
            case io.IOBase():
                pass
            case _:
                assert False, f"binarydata should be a byte array or a readable binary file object/TCP/UDP socket, but was `{type(binarydata)}´"

        match identifier:
            case str():
                try:
                    rVal = self.constructs[identifier].parse_stream(binarydata)
                except KeyError:
                    assert False, f"could not find construct `{identifier}´"
            case construct.Construct():
                rVal = identifier.parse_stream(binarydata)
            case _:
                assert False, f"identifier should be a string or a construct.Construct, but was `{type(identifier)}´"
        robot.api.logger.info(f"""parsed: {rVal} using {identifier} from {binarydata}""")
        return rVal

    @keyword('Generate binary from `${data}´ using construct `${identifier}´')
    def generate_binary_data_using_construct(self, data: typing.Union[dict, construct.Struct], identifier: typing.Union[str, construct.Construct]) -> bytes:
        """Generates a bytearray from a dictionary using construct.

        Arguments:
        | =Arguments= | =Description= |
        | data        | The dictionary to be used for generating the binary data |
        | identifier  | The construct to be used for generating, either as registered with 'Register construct' or a construct type variable |
        """
        match identifier:
            case str(_):
                rVal = self.constructs[identifier].build(data)
            case construct.Construct():
                rVal = identifier.build(data)
        robot.api.logger.info(f"""built: {rVal} using `{identifier}´ from `{data}´""")
        return rVal

    @keyword('Write binary data generated from `${data}´ using construct `${identifier}´ to `${file}`')
    def write_binary_data_using_construct(self, data: dict, identifier: typing.Union[dict, construct.Struct], file: io.IOBase) -> None:
        """Writes binary data to a file or sends it over a socket.

        Arguments:
        | =Arguments= | =Description= |
        | data        | The dictionary to be used for generating the binary data |
        | identifier  | The construct to be used for generating, either as registered with 'Register construct' or a construct variable |
        | file        | The file to write the binary data to, either a file object or a socket |
        """
        match identifier:
            case str(_):
                rVal = (self.constructs[identifier].build(data))
            case construct.Construct():
                rVal = identifier.build(data)
        robot.api.logger.info(f"""built: {rVal} using `{identifier}´ from `{data}´""")
        match file:
            case io.IOBase():
                file.write(rVal)
            case socket.socket():
                file.send(rVal)

    @keyword('Open `${filepath}´ for reading binary data')
    def open_binary_file_to_read(self, filepath: typing.Union[str, pathlib.Path]) -> io.IOBase:
        """Opens a file filepath for reading binary data.

        Arguments:
        | =Arguments= | =Description= |
        | filepath    | The path to the file to be opened |
        """
        return open(filepath, "rb")

    @keyword('Open `${filepath}´ for writing binary data')
    def open_binary_file_to_write(self, filepath: typing.Union[str, pathlib.Path]) -> io.IOBase:
        """Opens a file filepath for writing binary data.
        
        Arguments:
        | =Arguments= | =Description= |
        | filepath    | The path to the file to be opened |
        """
        return open(filepath, "wb")

    @keyword('Open ${protocol} connection to server `${server}´ on port `${port}´')
    def open_socket(self, protocol: Protocol, server:str, port:int) -> socket.socket:
        """Opens a connection to the server server on port port using protocol.

        Arguments:
        | =Arguments= | =Description= |
        | protocol    | The protocol to be used, either `TCP´ or `UDP´ |
        | server      | The server to connect to, either an ip adress or a hostname |
        | port        | The port to connect to |
        """
        match protocol:
            case Protocol.TCP:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((server, port))
                return s
            case Protocol.UDP:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect((server, port))
                _port_mapping[port] = s.getsockname()[1]
                return s
            case _:
                assert False, f"protocol should be either `TCP or `UDP´, but was `{protocol}´"
