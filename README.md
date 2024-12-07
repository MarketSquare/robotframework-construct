![PyPI](https://img.shields.io/pypi/v/robotframework-construct)
![Build](https://github.com/MarketSquare/robotframework-construct/actions/workflows/main.yml/badge.svg)
![Mutation Testing](https://github.com/MarketSquare/robotframework-construct/actions/workflows/mutations.yml/badge.svg)
![Breakout to C++ example](https://github.com/MarketSquare/robotframework-construct/actions/workflows/pythonBreakout.yml/badge.svg)
![radon maintainabity check](https://github.com/MarketSquare/robotframework-construct/actions/workflows/run_radon.yml/badge.svg)
![ruff check](https://github.com/MarketSquare/robotframework-construct/actions/workflows/run_ruff.yml/badge.svg)

# robotframework-construct

## I am in a hurry, let's jump-start with an example!
[git](https://github.com/astral-sh/uv) and [uv](https://github.com/astral-sh/uv) need to be preinstalled to run the examples.

```bash
git clone https://github.com/MarketSquare/robotframework-construct.git
cd robotframework-construct
uv tool install xonsh
uvx xonsh tasks/baseQC.xsh 
```


## What is robotframework-construct?
robotframework-construct is a [Robot Framework](https://robotframework.org) keyword library powered by [construct](https://construct.readthedocs.io/en/latest/).

[construct](https://construct.readthedocs.io/en/latest/) is a declarative and symmetrical parser and builder for binary data.

Aiming for :rocket: speed, :white_check_mark: reliability, and :microscope: visibility.

Your binary data becomes as accessible as numbers and strings are in Robot Framework.

Checkout the documentation at [robotframework-construct](https://marketsquare.github.io/robotframework-construct/)
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
    "size" / Rebuild(Int32sl, _calc_size),
    "elements" / _e_list,
    "EOO" / Const(b"\x00")
)
```

This can be readily and directly derived from the bson specification [bson specification](https://bsonspec.org/spec.html). AI can help do that, efficiently. This is because the mapping between the specification and the declaration is immediate making it easy to supervise the process and verify the result.

Using AI to generate a parser+generator would result in a larger volume of code to be verified, and the verification is harder.

### Checking and modifying binary data
There are keywords with embedded parameters allowing checking and modifying binary data in a robotframework way

A checking example
![image](https://github.com/user-attachments/assets/9d01b19d-480a-4393-9cca-1060f3e54712)

and a modifying example
![image](https://github.com/user-attachments/assets/55de01cf-09b5-4ad7-ab46-02aa718dc8db)

note, that this is very natural in the robotframework environment. If multiple elements need to be checked, this needs to be organized in keywords.

### Observing the binary data
The binary data built and parsed is easily accessible. This helps with trust issues and makes it easier
to read digital analyzer outputs or oscilloscope screens. Also, a name to identify what definition is doing the parsing/generating is provided.

A building example.:

![image](https://github.com/user-attachments/assets/9ad060cc-54cd-487e-9cb6-e0798aa53702)


A parsing example.:

![image](https://github.com/user-attachments/assets/041852dc-ff40-4ade-9d3c-0999c5057cd1)

### Breaking out of the ecosystems
The highly valuable building/parsing infrastructure does not depend on robotframework, and in the case of the parsing part, it also does not depend on Python.
The Structs can be transformed into kaitai. Kaitai is a DSL that can be transformed into parsers in 10+ languages and counting [https://kaitai.io/].

Keep in mind that some limitations apply to these transformations.

For reference.: [./tasks/breakoutCpp.xsh] which creates a C++ parser

## Relationships in the Ecosystem

The number of dependencies is kept low, with no transient dependencies.

This is important as it keeps coordination feasible. Construct is well-developed and not expected to change significantly soon. Robot Framework releases major updates annually, but these are well-managed and communicated.

### [Construct](https://github.com/construct/construct)

All parsing and generating capabilities come from Construct. No additional parsing/generating code is added; the only code added interfaces Construct with Robot Framework. The way Construct objects are created remains unchanged.

Construct has no non-optional dependencies.

### [Robot Framework](https://robotframework.org/)

This project connects Construct with Robot Framework. Only official APIs are used, and this project depends entirely on Robot Framework.

Robot Framework has no non-optional dependencies.

### [Rammbock](https://github.com/MarketSquare/Rammbock)

Rammbock inspired this project, as it was one of the reasons I started using Robot Framework.

Instead of maintaining Rammbock, we chose to integrate Construct.

#### Reasoning

Both Rammbock and Construct have limited engineering resources, but Construct is currently better supported. Construct also collaborates with Kaitai, engaging communities in C#, C++, and other ecosystems.

Using Construct provides a clear separation between parsing/generating logic and interface code, enabling expansion into other ecosystems.

## Installation

The robotframework-construct keyword library is hosted on pypi and can be installed like any pypi hosted python dependency with pip.

```
pip install robotframework-construct
```

## Limitations

Construct declarations must be written in `.py` files. There are no plans to integrate the Construct DSL into Robot Framework.

This eases the breaking out of the robot-framework and Python ecosystems.

## Quality Control Measures

Tested examples and acceptance tests using Robot Framework are provided. Unit tests are not a priority.

### Mutation Testing

Since this project consists primarily of interface code, it is crucial to catch user errors and produce clear error messages. Mutation testing ensures that all code paths and error messages are tested, supporting efforts to make errors informative.

## Project To-Do List

- [x] Parsing functionality demonstrated with an in-memory BSON object.
- [x] Parsing functionality demonstrated with a BSON file.
- [x] Generating functionality demonstrated with an in-memory BSON object.
- [x] Generating functionality demonstrated with a binary file.
- [x] Register read/write demonstrated with a mockup register.
- [x] Receive/transmit network example using DNS.
- [x] Reflector tool to allow to implement servers using clients.
- [x] Upload wheel to pypi.
- [x] Increase test coverage (Mutant killing) of the reflector
- [x] Segmentise mutation testing to speedup
- [x] Comment and document the real world example with the USB HID keyboard
- [x] Add a second real world example with binary interface to Readme
- [x] Have libdoc documentation online
- [x] Have libdoc documentation online for all keywords, not only the central ones
- [ ] User guide and tutorials/Article for (https://medium.com/@RobotFramework/).
- [x] Example on how to breakout of the python ecosystem
- [x] Midway review with Robot Framework Foundation.
- [ ] Final review with Robot Framework Foundation.
