*** Settings ***
Documentation      This is a simple example for a robot file using robotframework-construct demonstrating the regmap feature
Library            robotframework_construct.regmap
Test Setup         prepare regmaps
Test Tags          mutation_regmap
*** Test Cases ***
negative loading regmaps
    Run Keyword And Expect Error    All elements of the construct regmap need to have an identifiable name    Register regmap `empty_name´ from `math_coprocessor_regmap´ for `dsp1´
    Run Keyword And Expect Error    All elements of the construct regmap need to have an identifiable name    Register regmap `no_name´ from `math_coprocessor_regmap´ for `dsp1´
    Register regmap `math_coprocessor_map´ from `math_coprocessor_regmap´ for `dsp1´
    Run Keyword And Expect Error     not overwriting regmap*       Register regmap `math_coprocessor_map´ from `math_coprocessor_regmap´ for `dsp1´
    Register read register access function `read_register´ from `math_coprocessor_model´ for `dsp1´
    Run Keyword And Expect Error     not overwriting*       Register read register access function `read_register´ from `math_coprocessor_model´ for `dsp1´
    Register write register access function `write_register´ from `math_coprocessor_model´ for `dsp1´
    Run Keyword And Expect Error     not overwriting*       Register write register access function `write_register´ from `math_coprocessor_model´ for `dsp1´
    Run Keyword And Expect Error    All elements of the construct regmap need to have the same size     Register regmap `regmap_inconsistent_length´ from `math_coprocessor_regmap´ for `dsp2´
    Run Keyword And Expect Error    The construct regmap needs to have at least one element             Register regmap `empty_regmap´ from `math_coprocessor_regmap´ for `dsp2´

Example Test Case
    Read register `0` from `dsp´
    Read register `opcode` from `dsp´
    Write register `operand1` in `dsp´ with `${123}´
    Write register `operand2` in `dsp´ with `${123}´
    Write register `0` in `dsp´ with `${{ {"add": 1, "sub": 0, "mul": 0, "div": 0} }}´
    Read register `3` from `dsp´
    Write register `0` in `dsp´ with `${{ {"add": 0, "sub": 1, "mul": 0, "div": 0} }}´
    Read register `3` from `dsp´
    Write register `0` in `dsp´ with `${{ {"add": 0, "sub": 0, "mul": 1, "div": 0} }}´
    Read register `3` from `dsp´
    Write register `0` in `dsp´ with `${{ {"add": 0, "sub": 0, "mul": 0, "div": 1} }}´
    Read register `3` from `dsp´
    ${reg0}=      Read register `0` from `dsp´
    Get elemement `div´ from `${reg0}´
    ${reg0}=      Modify the elemement located at `div´ of `${reg0}´ to `${0}´
    ${reg0}=      Modify the elemement located at `add´ of `${reg0}´ to `1´
    Write register `0` in `dsp´ with `${reg0}´
    Read register `3` from `dsp´

remove and reload check
    Remove register map `dsp´
    Register regmap `math_coprocessor_map´ from `math_coprocessor_regmap´ for `dsp´

Write register with bad data
    Read register `opcode` from `dsp´
    Run Keyword And Expect Error    could not find register*     Read register `cheese` from `dsp´
    Run Keyword And Expect Error    could not find register*     Read register `123` from `dsp´
    Run Keyword And Expect Error    could not build data with*   Write register `operand1` in `dsp´ with `one´

*** Keywords ***
prepare regmaps
    Register regmap `math_coprocessor_map´ from `math_coprocessor_regmap´ for `dsp´
    Register read register access function `read_register´ from `math_coprocessor_model´ for `dsp´
    Register write register access function `write_register´ from `math_coprocessor_model´ for `dsp´
