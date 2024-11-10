from robotframework_construct import Protocol, _port_mapping
import socket
import select
import threading
from robot.api.deco import keyword
import robot.api.logger
import queue


def _reflect(protocol: Protocol, coms: threading.Event, portQ: queue.Queue) -> None:
        protocolType = {Protocol.TCP: socket.SOCK_STREAM, Protocol.UDP: socket.SOCK_DGRAM}[protocol]

        with socket.socket(socket.AF_INET, protocolType) as s1, socket.socket(socket.AF_INET, protocolType) as s2:
            initialSockets = [s1, s2]
            match protocol:
                case Protocol.TCP:
                    for s in initialSockets:
                        s.bind(('', 0))
                        s.listen(1)
                        s.setblocking(False)
                    
                    ports = tuple([s.getsockname()[1] for s in initialSockets])
                    portQ.put(ports)

                    toAccept = set(initialSockets)
                    conns = []
                    while toAccept and False is coms.is_set():
                        recvAble, _, __ =  select.select(toAccept, [], [], 1)
                        toAccept = toAccept ^ set(recvAble)
                        conns.extend([s.accept()[0] for s in recvAble])
                    while False is coms.is_set():
                        conDict = {conns[0]: conns[1], conns[1]: conns[0]}
                        recvAble, _, __ =  select.select(conDict.values(), [], [], 1)
                        for s in recvAble:
                            conDict[s].send(s.recv(0x80000000))

                case Protocol.UDP:
                    for s in initialSockets:
                        s.bind(('', 0))
                        s.setblocking(False)
                    
                    ports = tuple([s.getsockname()[1] for s in initialSockets])
                    portQ.put(ports)
                    conDict = {s1: s2, s2: s1}
                    portDict = {key: value for key, value in zip([s2, s1], ports)}
                    while False is coms.is_set():
                        recvAble, _, __ =  select.select(initialSockets, [], [], 1)
                        for s in recvAble:
                            data, _ = s.recvfrom(0x80000000)
                            conDict[s].sendto(data, ("localhost", _port_mapping[portDict[s]]))

class reflector:
    def __init__(self):
        self._please_die = threading.Event()
        self._please_die.clear()
        self._thread = None
        self._port1 = None
        self._port2 = None
        self._protocol = None

    @keyword("Reflect traffic between ports using `${protocol}´")
    def reflector(self, protocol: Protocol) -> None:
        """Reflects data between two ports.

        `port1` is the port to listen to and `port2` is the port to reflect data to.
        `protocol` can be either `TCP` or `UDP`.

        Only exactly one connection is allowed per port. No reconnects, No multiple connections.

        Example:
        Reflect traffic between ports `9090´ and `9191´ using `TCP´"
        """
        assert self._thread is None, "Reflector is already running"
        portQ = queue.Queue()
        self._thread = threading.Thread(target=_reflect, daemon=True, args=(protocol, self._please_die, portQ)).start()
        port1, port2 = portQ.get()
        self._port1    = port1
        self._port2    = port2
        self._protocol = protocol
        robot.api.logger.info(f"Reflector started on ports {port1} and {port2} using {protocol}")
        return (port1, port2,)
    
    def shutdown_reflector(self):
        """Terminates this reflector

        Example:
        Shutdown Reflector
        """
        self._please_die.set()
        self._thread.join()
        self._thread = None
        self._please_die.clear()
        robot.api.logger.info(f"Reflector terminated on ports {self._port1} and {self._port2} using {self._protocol}")
        self._port1 = None
        self._port2 = None
        self._protocol = None
