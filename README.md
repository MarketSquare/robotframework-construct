# robotframework-construct

## What is robotframework-construct?

[Robot Framework](https://robotframework.org) library powered by [construct](https://construct.readthedocs.io/en/latest/).

A declarative and symmetrical parser and builder for binary data.

Aiming for :rocket: speed, :white_check_mark: reliability, and :microscope: visibility.

Ideally, your binary data becomes as accessible as numbers and strings are in Robot Framework.

Checkout the documentation at [robotframework-construct](https://marketsquare.github.io/robotframework-construct/)

### Use cases

- Test your production construct specification against a reference implementation of the same protocol.
- Test your production binary parser/generator against a construct implementation of your binary format.
- Use your construct specification to:
  - Craft intentionally corrupted data.
  - Fuzz test your binary parsers.
- Beautifuly access registers, for both reading and writing.

## Relationships in the Ecosystem

The number of dependencies is kept low, with no transient dependencies.

This is important as it keeps coordination feasible. Construct is well-developed and not expected to change significantly soon. Robot Framework releases major updates annually, but these are well-managed and communicated.

### Construct (https://github.com/construct/construct)

All parsing and generating capabilities come from Construct. No additional parsing/generating code is added; the only code added interfaces Construct with Robot Framework. The way Construct objects are created remains unchanged.

Construct has no non-optional dependencies.

### Robot Framework (https://robotframework.org/)

This project connects Construct with Robot Framework. Only official APIs are used, and this project depends entirely on Robot Framework.

Robot Framework has no non-optional dependencies.

### Rammbock (https://github.com/MarketSquare/Rammbock)

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

To maintain reusability, Construct specifications must be written in `.py` files. There are no plans to integrate the Construct DSL into Robot Framework.

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
- [ ] Comment and document the real world example with the USB HID keyboard
- [ ] Add a second real world example with binary interface to Readme
- [x] Have libdoc documentation online
- [x] Have libdoc documentation online for all keywords, not only the central ones
- [ ] User guide and tutorials/Article for (https://medium.com/@RobotFramework/).
- [x] Example on how to breakout of the python ecosystem
- [ ] Midway review with Robot Framework Foundation.
- [ ] Final review with Robot Framework Foundation.
