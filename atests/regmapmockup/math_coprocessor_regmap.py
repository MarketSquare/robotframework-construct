import construct


math_coprocessor_map = construct.Struct(
        "opcode"  / construct.BitStruct("add" / construct.Flag,
                                        "sub" / construct.Flag,
                                        "mul" / construct.Flag,
                                        "div" / construct.Flag,
                                        "pad" / construct.Padding(28)),
        "operand1" / construct.Int32sl,
        "operand2" / construct.Int32sl,
        "result"   / construct.Int32sl,
    )


math_coprocessor_map_inconsistent_length = construct.Struct(
        "opcode"  / construct.BitStruct("add" / construct.Flag,
                                        "sub" / construct.Flag,
                                        "mul" / construct.Flag,
                                        "div" / construct.Flag,
                                        "pad" / construct.Padding(36)),
        "operand1" / construct.Int32sl,
        "operand2" / construct.Int32sl,
        "result"   / construct.Int32sl,
    )

empty_regmap = construct.Struct(
        "opcode"  / construct.BitStruct("add" / construct.Flag,
                                        "sub" / construct.Flag,
                                        "mul" / construct.Flag,
                                        "div" / construct.Flag,
                                        "pad" / construct.Padding(36)),
        "operand1" / construct.Int32sl,
        "operand2" / construct.Int32sl,
        "result"   / construct.Int32sl,
    )
empty_regmap.subcons = []

regmap_inconsistent_length = construct.Struct(
        "opcode"  / construct.BitStruct("add" / construct.Flag,
                                        "sub" / construct.Flag,
                                        "mul" / construct.Flag,
                                        "div" / construct.Flag,
                                        "pad" / construct.Padding(36)),
        "operand1" / construct.Int32sl,
        "operand2" / construct.Int32sl,
        "result"   / construct.Int32sl,
    )
empty_name = construct.Struct(
        "opcode"  / construct.BitStruct("add" / construct.Flag,
                                        "sub" / construct.Flag,
                                        "mul" / construct.Flag,
                                        "div" / construct.Flag,
                                        "pad" / construct.Padding(36)),
        "operand1" / construct.Int32sl,
        "operand2" / construct.Int32sl,
        "result"   / construct.Int32sl,
    )

no_name = construct.Struct(
        "opcode"  / construct.BitStruct("add" / construct.Flag,
                                        "sub" / construct.Flag,
                                        "mul" / construct.Flag,
                                        "div" / construct.Flag,
                                        "pad" / construct.Padding(4)),
        "operand1" / construct.Int32sl,
        "operand2" / construct.Int32sl,
        "result"   / construct.Int32sl,
    )

class noName:
    pass

no_name.subcons[1] = noName()
empty_name.subcons[1].name = ""
