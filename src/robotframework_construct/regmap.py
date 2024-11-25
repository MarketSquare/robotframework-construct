from robot.api.deco import keyword
import robot.api.logger
import importlib
import construct
import collections
from robotframework_construct import _construct_interface_basics
import typing


class _regmap_entry:
    regmap: construct.Construct = None
    read_reg: typing.Union[None, typing.Callable] = None
    write_reg: typing.Union[None, typing.Callable] = None


class regmap(_construct_interface_basics):

    def __init__(self):
        self._regmaps = collections.defaultdict(_regmap_entry)
        super().__init__()

    def _get_subcon(self, reg, identifier):
        try:
            subconNames = [i.name for i in self._regmaps[identifier].regmap.subcons]
            relevantStruct = getattr(self._regmaps[identifier].regmap, reg)
            reg = subconNames.index(reg)
        except AttributeError:
            try:
                reg = int(reg)
            except ValueError:
                assert False, f"could not find register {reg} in regmap {identifier}, neither an Integer nor a member of {', '.join(subconNames)}"
            try:
                relevantStruct = self._regmaps[identifier].regmap.subcons[reg]
            except IndexError:
                assert False, f"could not find register {reg} in regmap {identifier}, register out of bound"
        return reg,relevantStruct

    @keyword('Remove register map `${identifier}´')
    def remove_register_map(self, identifier: str):
        del self._regmaps[identifier]

    @keyword('Register regmap `${spec}´ from `${library}´ for `${identifier}´')
    def register_regmap(self, spec: str, library: str, identifier: str):
        lib = importlib.import_module(library)
        spec = getattr(lib, spec)
        assert isinstance(spec, construct.Construct), f"spec should be a Construct, but was {type(spec)}"
        assert not isinstance(spec, construct.core.Compiled), f"spec must not be a compiled Construct, but was {type(spec)}"
        assert len(spec.subcons), "The construct regmap needs to have at least one element"
        assert all(hasattr(item, "name") and isinstance(item.name, str) and len(item.name) for item in spec.subcons), "All elements of the construct regmap need to have an identifiable name"
        assert self._regmaps[identifier].regmap is None, f"not overwriting regmap {identifier}"
        assert len(set(item.sizeof() for item in spec.subcons)) in {1}, "All elements of the construct regmap need to have the same size"

        self._regmaps[identifier].regmap = spec

    @keyword('Register read register access function `${spec}´ from `${library}´ for `${identifier}´')
    def register_read_register_access_function(self, spec: str, library: str, identifier: str):
        lib = importlib.import_module(library)
        spec = getattr(lib, spec)
        assert callable(spec), f"spec should be a callable, but was {type(spec)}"
        assert self._regmaps[identifier].read_reg is None, f"not overwriting read_reg for {identifier}"
        self._regmaps[identifier].read_reg = spec

    @keyword('Register write register access function `${spec}´ from `${library}´ for `${identifier}´')
    def register_write_register_access_function(self, spec: str, library: str, identifier: str):
        lib = importlib.import_module(library)
        spec = getattr(lib, spec)
        assert callable(spec), f"spec should be a callable, but was {type(spec)}"
        assert self._regmaps[identifier].write_reg is None, f"not overwriting write_reg for {identifier}"
        self._regmaps[identifier].write_reg = spec

    @keyword('Read register `${reg}` from `${identifier}´')
    def read_register(self, reg, identifier: str):
        reg, relevantStruct = self._get_subcon(reg, identifier)
        regVal = self._regmaps[identifier].read_reg(reg)
        assert isinstance(regVal, bytes), f"read register should return bytes, but returned {type(regVal)}"
        return relevantStruct.parse(regVal)

    @keyword('Write register `${reg}` in `${identifier}´ with `${data}´')
    def write_register(self, reg: typing.Any, identifier: str, data: typing.Union[bytes, dict, construct.Struct]):
        reg, relevantStruct = self._get_subcon(reg, identifier)
        if isinstance(data, bytes):
            dataOut = data
            robot.api.logger.info(f"""writing: {dataOut!r} using `{identifier}´ from `{data!r}´ unmodified""")
        else:
            try:
                dataOut = relevantStruct.build(data)
            except (construct.core.ConstructError, KeyError, IndexError) as e:
                assert False, f"could not build data with {relevantStruct} due to {e}"
            robot.api.logger.info(f"""built: {dataOut!r} using `{identifier}´ from `{data!r}´""")
        return self._regmaps[identifier].write_reg(reg, dataOut)
