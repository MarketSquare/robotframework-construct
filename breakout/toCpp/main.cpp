#include <fstream>
#include <iostream>
#include "regmap.h"

int main() {
    std::ifstream file("example.bin", std::ifstream::binary);
    
    if (!file) {
        std::cerr << "Cannot open file!" << std::endl;
        return 1;
    }

    kaitai::kstream ks(&file);
    regmap_t outer(&ks);

    regmap_t::type_1_t parsed = *outer.opcode();

    std::cout << "add: " << parsed.add() << std::endl;
    std::cout << "sub: " << parsed.sub() << std::endl;
    std::cout << "mul: " << parsed.mul() << std::endl;
    std::cout << "div: " << parsed.div() << std::endl;

    std::cout << std::endl;

    return 0;
}
