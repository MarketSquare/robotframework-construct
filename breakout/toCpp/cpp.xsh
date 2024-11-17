import itertools


cd breakout/toCpp


exec(open('../../atests/regmapmockup/math_coprocessor_regmap.py').read())

wget https://github.com/kaitai-io/kaitai_struct_compiler/releases/download/0.10/kaitai-struct-compiler-0.10.zip
unzip kaitai-struct-compiler-0.10.zip -d ksc
wget https://github.com/kaitai-io/kaitai_struct_cpp_stl_runtime/archive/refs/tags/0.10.1.tar.gz
tar -xvf 0.10.1.tar.gz

with open("regmap.ksy", "w") as f:
    f.write(math_coprocessor_map.export_ksy("regmap"))

./ksc/kaitai-struct-compiler-0.10/bin/kaitai-struct-compiler --target cpp_stl -d regmap.ksy

clang++ -DKS_STR_ENCODING_NONE -c -I kaitai_struct_cpp_stl_runtime-0.10.1/ regmap.cpp main.cpp kaitai_struct_cpp_stl_runtime-0.10.1/kaitai/kaitaistream.cpp
clang++ -o regmap regmap.o main.o kaitaistream.o

for add, sub, mul, div in itertools.product([0, 1], repeat=4):
    obj = {"opcode": {"add": add, "sub": sub, "mul": mul, "div": div, "pad": 0}, "operand1": 1, "operand2":2, "result": 0}
    print(f"build using construct: {obj}")
    math_coprocessor_map.build_file(obj, f"./example.bin")
    r = !(./regmap)
    print(f"parsed with cpp:\n{r}")
    print("================================================================")
    print()

