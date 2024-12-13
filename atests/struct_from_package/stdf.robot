*** Settings ***
Documentation  This example shows how without any additional code a construct based library can be repurposed for robotframework. 
...            The stdf-tamer predates robotframework-construct and there was no coordination or change necessary to reuse the structs.
...
...            Stdf files are used in the semiconductor industry to store test data. The stdf-tamer library is a python library that
...            can read and write stdf files.
Library        ams_rw_stdf_writer
Library        robotframework_construct
*** Test Cases ***
write a stdf file using ams_rw_stdf_writer and check with robotframework-construct
    ${STDF_HANDLE}=           Start Stdf File     stdf_file_name=${OUTPUT DIR}/example.stdf    part_type=type     lot_id=lot  operator=operator     test_setup_id=id    test_cod=cod     tp_version=x;;
    Start Sample                        ${STDF_HANDLE}
    Finish Sample                       ${STDF_HANDLE}         dummy

    Register construct 'RECORD' from 'ams_rw_stdf' as 'stdf_record'
    ${IFILE}=           Open '${OUTPUT DIR}/example.stdf' for reading binary data
    ${returnedDict}=        Parse '${IFILE}' using construct 'stdf_record'
    Element 'PL.STDF_VER' in '${returnedDict}' should be equal to '${{b"\x04"}}'
    ${returnedDict}=        Parse '${IFILE}' using construct 'stdf_record'
    Element 'PL.TEST_COD' in '${returnedDict}' should be equal to 'cod'
    ${returnedDict}=        Parse '${IFILE}' using construct 'stdf_record'
    Element 'REC_SUB' in '${returnedDict}' should be equal to '10'
    Element 'PL.HEAD_NUM' in '${returnedDict}' should be equal to '1'
    Element 'PL.SITE_NUM' in '${returnedDict}' should be equal to '1'
    ${returnedDict}=        Parse '${IFILE}' using construct 'stdf_record'
    Element 'PL.HEAD_NUM' in '${returnedDict}' should be equal to '1'
    Element 'PL.SITE_NUM' in '${returnedDict}' should be equal to '1'
    Element 'REC_SUB' in '${returnedDict}' should be equal to '20'
    ${returnedDict}=        Parse '${IFILE}' using construct 'stdf_record'
    Element 'PL.HEAD_NUM' in '${returnedDict}' should be equal to '1'
    Element 'PL.SITE_NUM' in '${returnedDict}' should be equal to '1'
    Element 'REC_SUB' in '${returnedDict}' should be equal to '40'
    ${returnedDict}=        Parse '${IFILE}' using construct 'stdf_record'
    Element 'PL.HEAD_NUM' in '${returnedDict}' should be equal to '1'
    Element 'PL.SITE_NUM' in '${returnedDict}' should be equal to '1'
    Element 'REC_SUB' in '${returnedDict}' should be equal to '50'
    ${returnedDict}=        Parse '${IFILE}' using construct 'stdf_record'
    Element 'REC_TYP' in '${returnedDict}' should be equal to '1'
    Element 'REC_SUB' in '${returnedDict}' should be equal to '20'
