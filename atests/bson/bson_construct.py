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
document.name = "bson document"
