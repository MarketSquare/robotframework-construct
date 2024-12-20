![PyPI](https://img.shields.io/pypi/v/robotframework-construct)
![Build](https://github.com/MarketSquare/robotframework-construct/actions/workflows/main.yml/badge.svg)
![Mutation Testing](https://github.com/MarketSquare/robotframework-construct/actions/workflows/mutations.yml/badge.svg)
![Breakout to C++ example](https://github.com/MarketSquare/robotframework-construct/actions/workflows/pythonBreakout.yml/badge.svg)
![radon maintainability check](https://github.com/MarketSquare/robotframework-construct/actions/workflows/run_radon.yml/badge.svg)
![ruff check](https://github.com/MarketSquare/robotframework-construct/actions/workflows/run_ruff.yml/badge.svg)

# robotframework-construct

## I am in a hurry, let's jump-start with an example!
[git](https://git-scm.com/) (a version control system) and [uv](https://github.com/astral-sh/uv) (a tool for managing Python virtual environments) need to be preinstalled to run the examples.

```bash
git clone https://github.com/MarketSquare/robotframework-construct.git
cd robotframework-construct
uv sync --extra test --dev
uv run xonsh tasks/baseQC.xsh
```

Some examples, such as [USB HID](./atests/HIDKeyboard/) and [this](./atests/nfc_nci/), require specific hardware to function. For the [this](./atests/nfc_nci/) example, STMicroelectronics hardware and firmware is required. For the HID example, a USB Keyboard on a Linux machine is sufficient.

## What is robotframework-construct?
robotframework-construct is a [Robot Framework](https://robotframework.org) keyword library powered by [construct](https://construct.readthedocs.io/en/latest/).

[construct](https://construct.readthedocs.io/en/latest/) is a declarative and symmetrical parser and builder for binary data.

Aiming for :rocket: speed, :white_check_mark: reliability, and :microscope: visibility.

Your binary data becomes as accessible as numbers and strings are in Robot Framework.

Check out the documentation [here](https://marketsquare.github.io/robotframework-construct/)
### Licensing
robotframework-construct is an opensource keyword library licensed under Apache-2.0, leveraging the [construct](https://construct.readthedocs.io/en/latest/) library licensed under MIT.

## Use cases

- Beautifully access registers, for both reading and writing.
- Test your production construct specification against a reference implementation of the same protocol.
- Test your production binary parser/generator against a construct implementation of your binary format.
- Use your construct declarations to:
  - Craft intentionally corrupted data.
  - Fuzz test your binary parsers.
- While the network is an interesting area for robotframework-construct, other interfaces (UART/SPI/I2C) are considered first-class citizen.

## Features

Check out the full documentation at [robotframework-construct](https://marketsquare.github.io/robotframework-construct/).

### From construct, declaration not implementation of a parser/generator

This is a real-world usable declaration of the bson protocol.

```python
from construct import Struct, Int8ul, Int32sl, Int64sl, Int64ul, Float64l, Const, Array, Byte, GreedyBytes, CString, Prefixed, Switch, LazyBound, Pass, GreedyRange, Rebuild, this


_bson_element = Struct(
    "type" / Int8ul,
    "name" / CString("utf8"),
    "value" / Switch(this.type, {
         1: Float64l,
         2: Prefixed(Int32sl, CString("utf8")),
         3: LazyBound(lambda: document),
         4: LazyBound(lambda: document),
         5: Prefixed(Int32sl, GreedyBytes),
         6: Pass,
         7: Array(12, Byte),
         8: Int8ul,
         9: Int64sl,
        10: Pass,
        11: Struct("pattern" / CString("utf8"), "options" / CString("utf8")),
        12: Struct("namespace" / CString("utf8"), "id" / Array(12, Byte)),
        13: Prefixed(Int32sl, CString("utf8")),
        14: Prefixed(Int32sl, CString("utf8")),
        15: Struct("code" / Prefixed(Int32sl, CString("utf8")), "scope" / LazyBound(lambda: document)),
        16: Int32sl,
        17: Int64ul,
        18: Int64sl,
        19: Array(16, Byte),
        -1: Pass,
        127: Pass,
    })
)
_e_list = GreedyRange(_bson_element)

def _calc_size(this):
    return  len(_e_list.build(this["elements"]))+5

document = Struct(
document = Struct(
    "size" / Rebuild(Int32sl, _calc_size),
    "elements" / _e_list,
    "EOO" / Const(b"\x00")
)
```

This can be readily and directly derived from the [bson specification](https://bsonspec.org/spec.html). AI can assist in this process efficiently. This is because the mapping between the specification and the declaration is a very direct and straightforward task, making it easy to supervise the process and verify the result.

Using AI to generate a parser+generator would result in a larger volume of code to be verified, and the verification is harder.

### Checking and modifying binary data
There are keywords with embedded parameters that allow checking and modifying binary data in a Robot Framework way

A checking example
![image](https://github.com/user-attachments/assets/9d01b19d-480a-4393-9cca-1060f3e54712)

and a modifying example
![image](https://github.com/user-attachments/assets/55de01cf-09b5-4ad7-ab46-02aa718dc8db)

**Note:** This is very natural in the Robot Framework environment. If multiple elements need to be checked, these checks should be organized in keywords.

### Observing the binary data
The built and parsed binary data is easily accessible. This helps with trust issues and makes it easier to read digital analyzer or oscilloscope screens. Also, a name to identify what definition is doing the parsing/generating may be provided.

A building example:

![image](https://github.com/user-attachments/assets/9ad060cc-54cd-487e-9cb6-e0798aa53702)

A parsing example:

![image](https://github.com/user-attachments/assets/041852dc-ff40-4ade-9d3c-0999c5057cd1)

### Breaking out of the ecosystems
The highly valuable building/parsing infrastructure does not depend on robotframework, and in the case of the parsing part, it also does not depend on Python.
The Structs can be transformed into kaitai. Kaitai is a DSL that can be transformed into parsers in 10+ languages and counting, you find further details [here](https://kaitai.io/).

Keep in mind that some limitations apply to these transformations.

For reference, a [script](./tasks/breakoutCpp.xsh) demonstrates how to transform Construct declarations into a C++ parser using the Kaitai DSL.

## Relationships in the Ecosystem

The number of dependencies is kept low, with no transitive dependencies.

This is important as it keeps coordination feasible. Construct is well-developed and not expected to change significantly soon. Robot Framework releases major updates annually, but these are well-managed and communicated.

### [Construct](https://github.com/construct/construct)

All parsing and generating capabilities come from Construct. No additional parsing/generating code is added; the only code added interfaces Construct with Robot Framework. The way Construct objects are created remains unchanged.

Construct has no non-optional dependencies.

### [Robot Framework](https://robotframework.org/)

This project connects Construct with Robot Framework. Only official APIs are used. This project depends on the Robot Framework.

Robot Framework has no non-optional dependencies.

### [Rammbock](https://github.com/MarketSquare/Rammbock)

Rammbock inspired this project, as it was one of the reasons I started using Robot Framework.

Instead of maintaining Rammbock, we chose to integrate Construct.

#### Reasoning

Rammbock and Construct have limited engineering resources, but Construct is currently better supported. Construct collaborates with Kaitai, engaging communities in C#, C++, and other ecosystems.

Using Construct provides a clear separation between parsing/generating logic and interface code, enabling expansion into other ecosystems.

## Installation

The robotframework-construct keyword library is hosted on pypi and can be installed like any pypi hosted python dependency with pip.

```
pip install robotframework-construct
```

## Limitations

Construct declarations must be written in `.py` files. The Construct DSL is not planned to be integrated into the Robot Framework.

This eases the breaking out of the Robot Framework and Python ecosystems.

## Quality Control Measures

Tested examples and acceptance tests using Robot Framework are provided. Unit tests are not a priority.

### Mutation Testing

Since this project primarily consists of interface code, catching user errors and producing clear error messages is crucial. Mutation testing ensures that all code paths and error messages are tested, supporting efforts to make errors informative.

## Project To-Do List

- [x] Parsing functionality demonstrated with an in-memory BSON object.
- [x] Parsing functionality demonstrated with a BSON file.
- [x] Generating functionality demonstrated with an in-memory BSON object.
- [x] Generating functionality demonstrated with a binary file.
- [x] Register read/write demonstrated with a mockup register.
- [x] Receive/transmit network examples using DNS.
- [x] Reflector tool to allow to implement servers using clients.
- [x] Upload wheel to pypi.
- [x] Increase test coverage (Mutant killing) of the reflector
- [x] Segmentise mutation testing to speed up
- [x] Comment and document the real-world example with the USB HID keyboard
- [x] Add a second real-world example with a binary interface to Readme
- [x] Have libdoc documentation online
- [x] Have libdoc documentation online for all keywords, not only the central ones
- [ ] User guide and tutorials/Article for (https://medium.com/@RobotFramework/).
- [x] Example of how to break out of the Python ecosystem
- [x] Midway review with Robot Framework Foundation.
- [x] Final review with Robot Framework Foundation.
