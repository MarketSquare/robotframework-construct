*** Settings ***
Documentation      This are tests checking for sensible error messages.
...
...                This is usefull for quality controll and for trouble shooting. These examples might help to understand the error messages.
Library            robotframework_construct
Test Setup         prepare regmaps
Test Tags          mutation_regmap
*** Test Cases ***
check error messages when loading invalid constructs
    Run Keyword And Expect Error    All elements of the construct regmap need to have an identifiable name    Register regmap 'empty_name' from 'math_coprocessor_regmap' for 'dsp1'
    Run Keyword And Expect Error    All elements of the construct regmap need to have an identifiable name    Register regmap 'no_name' from 'math_coprocessor_regmap' for 'dsp1'

check errormessages when double registering a regmap
    Register write register access function 'write_register' from 'math_coprocessor_model' for 'dsp1'
    Run Keyword And Expect Error     not overwriting*                                                         Register write register access function 'write_register' from 'math_coprocessor_model' for 'dsp1'
    Run Keyword And Expect Error    All elements of the construct regmap need to have the same size           Register regmap 'regmap_inconsistent_length' from 'math_coprocessor_regmap' for 'dsp2'

check error message when registering a regmap with no elements
    Run Keyword And Expect Error    The construct regmap needs to have at least one element                   Register regmap 'empty_regmap' from 'math_coprocessor_regmap' for 'dsp2'

check error messages when accessing registers with bad identifiers
    Run Keyword And Expect Error    could not find register*                                                  Read register 'cheese' from 'dsp'
    Run Keyword And Expect Error    could not find register*                                                  Read register '123' from 'dsp'

check error messages when writing bad data to registers
    Run Keyword And Expect Error    could not build data with*                                                Write register 'operand1' in 'dsp' with '${{ {"add": 1.12, "sub": 1, "mul": 0, "div": 0} }}'

*** Keywords ***
prepare regmaps
    Register regmap 'math_coprocessor_map' from 'math_coprocessor_regmap' for 'dsp'
    Register read register access function 'read_register' from 'math_coprocessor_model' for 'dsp'
    Register write register access function 'write_register' from 'math_coprocessor_model' for 'dsp'
