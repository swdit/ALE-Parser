#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALE (Avid Log Exchange) Parser
Has two main functions:
1 .Generates pandas data Frame from ALE file that can be treated like a usual tab delimited csv file.
2. Writes pandas dataframe to ALE file reattaching the ALE header.

Both functions have a build in custom logger (swdit_logger) based on logging module.
The logger can be set to different log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).
If CRITICAL is set, no logging output will be generated.

There is another Function (FUNCTION 0) that is used in ale_read_parser and checks if the linebreaks in the Input file
are consistent.
If deprecated 'CR' line breaks are present, the function will exit with and output an error.

The ale_rewrite function will create a new file in a subfolder called "altered_ale" in the same directory as the
original file. The new file will have the same name as the original file with the addition of "_new_" and a timestamp.
The function will return the path to the new file.

The ale_rewrite function will always output consistent linebreaks (LF or CRLF) default is LF if no argument is set.

It is also recommended to set the encoding of the file to UTF-8. If no encoding is set, the function will try to
detect the encoding of the file. If the encoding cannot be detected, the function will exit with an error.

It is also recommended to pass the encoding of the original file to the ale_read_parser function.
More exotic encodings like "ISO-8859-1" or "ISO-8859-15" can cause special characters to be displayed incorrectly in
default UTF-8 mode.

Parse ALEs:
Reader:
- find all Lines that start with only two columns (headerdict)
- check for delimiter
- remember line number
- make sure everything is being read as string (no int, no float)
>> arguments: ale_file (filepath, log_level)
>> returns: delim, headerdict, dataframe, ale_file, encoding

Writer:
- write headerdict (lines with only two columns)
- write column names of dataframe
- write "Data" line
- write content of dataframe excluding column names
"""

from datetime import datetime
import pandas as pd
import subprocess
from printme import *
import chardet
from swdit_logger import get_logger


# FUNCTION 0: Check for proper linebreaks
def check_line_breaks(file_path):
    # Read file as binary
    with open(file_path, 'rb') as file:
        content = file.read()

    # Count the occurrences of different types of line breaks
    crlf_count = content.count(b'\r\n')  # Windows-style line breaks
    lf_count = content.count(b'\n') - crlf_count  # Unix/MacOS-style line breaks
    cr_count = content.count(b'\r') - crlf_count  # Old MacOS-style line breaks
    total_count = crlf_count + lf_count + cr_count

    # Check if line breaks are consistent
    if crlf_count != 0 and crlf_count == total_count:
        consistency = True
    elif lf_count != 0 and lf_count == total_count:
        consistency = True
    elif cr_count != 0 and cr_count == total_count:
        consistency = True
    else:
        consistency = False

    # Check if deprecated 'CR' line breaks are present and set CR to True if so
    cr = True
    if cr_count == 0:
        cr = False

    return {
        'CRLF (\\r\\n) Count': crlf_count,
        'LF (\\n) Count': lf_count,
        'CR (\\r) Count': cr_count,
        'Total Lines': crlf_count + lf_count + cr_count,
        'consistency': consistency,
        'CR': cr
    }


# FUNCTION 1: Read ALE file into pandas dataframe and headerdict
def ale_read_parser(ale_file, log_level="INFO"):   # provide file (filepath) of the ale file as argument
    # Set up logger
    logger = get_logger(__name__, level=log_level)
    logger.info(grey + f"logging startet - reading file: {ale_file}" + clrs)
    logger.info(grey + "Set 'log_level' to 'WARNING' or 'ERROR' to receive less logging output. "
                       "Set to 'CRITICAL' to receive no logging output" + clrs)

    if not ale_file.split(".")[-1] == "ale":
        logger.error(f"Error reading file {ale_file} - This is not a valid ALE-File")
        exit()
    # Check for proper linebreaks
    logger.info(grey + "Checking for proper linebreaks" + clrs)
    line_break_info = check_line_breaks(ale_file)
    if not line_break_info["consistency"]:
        logger.warning(yellow + "Linebreaks are not consistent" + clrs)
        logger.warning(yellow + str(line_break_info) + clrs)
    if line_break_info["CR"]:
        logger.error(red + f"Error in '{ale_file}' - Contains deprecated 'CR' line breaks " + clrs)
        logger.error(red + str(line_break_info) + clrs)
        exit()

    # Check encoding of file
    logger.info(grey + "Checking encoding of file" + clrs)
    encoding = chardet.detect(open(ale_file, 'rb').read())['encoding']
    encoding = encoding.lower().replace("ISO-", "iso")
    encoding = encoding.lower().replace(" ", "_").replace("-", "_")
    logger.debug(grey + f"Encoding of file is: {encoding}" + clrs)
    # First Read of the Original ALE and Check for Delimiter Status
    with open(ale_file, 'r', encoding=encoding, newline='') as ale:
        firstline = ale.readline()
        scndline = ale.readline()
        if "Heading" not in firstline:
            if "COMMAS" in firstline:
                delim = ","
                logger.debug(grey + "This is a comma separated ALE file" + clrs)
            elif "TABS" in firstline:
                delim = "\t"
                logger.debug(grey + "This is a tab separated ALE file" + clrs)
            else:
                logger.error(red + "@DELIM - This is not a valid ALE file" + clrs)
                logger.error(red + f"{firstline}" + clrs)
                exit()
        elif "Heading" in firstline:
            if "COMMAS" in scndline:
                delim = ","
                logger.debug(grey + "This is a comma separated ALE file" + clrs)
            elif "TABS" in scndline:
                delim = "\t"
                logger.debug(grey + "This is a tab separated ALE file" + clrs)
            else:
                logger.error(red + "@DELIM - This is not a valid ALE file" + clrs)
                logger.error(red + f"{firstline}" + clrs)
                exit()
        else:
            logger.error(red + f"Firstline-Error - This is not a valid ALE file" + clrs)
            logger.error(red + f"firstline: {firstline} scndline: {scndline}" + clrs)
            exit()

    def ale_parser_headerlines(ale_file_infu):
        headerdict_infu = {}
        skiprows_infu = []

        # 2nd Read of Original ALE and to red the Headerlines
        with open(ale_file_infu, 'r', encoding=encoding, newline='') as ale_infu:
            for idx, line in enumerate(ale_infu):
                # add idx and line to headerdict
                headerdict_infu[idx] = line
                # add idx to skiprows list
                skiprows_infu.append(idx)

                logger.debug(headerdict_infu)
                logger.debug(skiprows_infu)
                if "Column" in line:
                    skiprows_infu.append(idx + 2)
                    headerdict_infu[idx + 2] = "\n"
                    skiprows_infu.append(idx + 3)
                    headerdict_infu[idx + 3] = "Data\n"
                    break

        logger.debug(skiprows_infu)
        return headerdict_infu, skiprows_infu

    def getdataframe(ale_file_int, delim_infu):
        df = pd.read_csv(ale_file_int, delimiter=delim_infu, skiprows=skiprows, encoding=encoding, dtype=str)

        # Check for field with too many characters
        # Function to check length of each cell in the dataframe
        def check_length_250(cell):
            if isinstance(cell, str) and len(cell) > 250:
                logger.warning(yellow + f"@Avid-MC: A field has more than 250 characters! >>> {cell}" + clrs)

        df.map(check_length_250)

        # Check for characters that are not allowed in ALE files
        # Function to check length of each cell in the dataframe
        def check_characters(cell):
            if isinstance(cell, str) and not cell.isascii():
                logger.warning(yellow + f"@Avid-MC: A field has non-ASCII characters! >>> {cell}" + clrs)

        logger.info(grey + "Checking for non-ASCII characters" + clrs)
        df.map(check_characters)

        # Check if a column with the name "Clip-Name" exists.
        # Display warning if there are entries with more than 63 characters
        def check_length_63(name):
            if pd.isna(name):
                logger.warning(yellow + f" A field is empty or float and cannot be length-ckecked >>> {name}" + clrs)
            else:
                if len(name) > 63:
                    logger.warning(yellow + f"@Avid-MC: a field exceeds 63 characters '{name}'" + clrs)

        # Check if the column exists and apply the function

        if "Clip-Name" in df.columns:
            logger.info(grey + "Checking for Clip-Name length" + clrs)
            df["Clip-Name"].apply(check_length_63)
        elif "Clip_Name" in df.columns:
            logger.info(grey + "Checking for Clip_Name length" + clrs)
            df["Clip_Name"].apply(check_length_63)
        elif "Name" in df.columns:
            logger.info(grey + "Checking for Name length" + clrs)
            df["Name"].apply(check_length_63)
        else:
            logger.warning(yellow + "@Avid-MC: No column named 'Clip-Name' or 'Name' found" + clrs)

        # Check if a column with the name "Tape" exists and
        # Display warning if there are entries with more than 31 characters
        def check_length_31(name):
            if pd.isna(name):
                logger.warning(yellow + f" A field is empty or float and cannot be length-ckecked >>> {name}" + clrs)
            else:
                if len(name) > 31:
                    logger.warning(yellow + f"@Avid-MC: a field exceeds 31 characters '{name}'" + clrs)

        # Check if the column exists and apply the function
        if "Tape" in df.columns:
            logger.info(grey + "Checking for Tape length" + clrs)
            df["Tape"].apply(check_length_31)
        else:
            logger.warning(yellow + "@Avid-MC: No column named 'Tape' found" + clrs)

        return df

    # execute funktion for delimiter and headerlines and return variables
    headerdict, skiprows = ale_parser_headerlines(ale_file)  # execute funktion for delimiter and headerlines
    dataframe = getdataframe(ale_file, delim)  # execute funktion for main dataframe
    return delim, headerdict, dataframe, ale_file, encoding


# FUNCTION 2: Write pandas dataframe to ALE file reattaching the ALE header.
def ale_rewrite(ale_path, delim, headerdict, dataframe, encoding="utf-8", newline='\n', log_level="INFO"):
    logger = get_logger(__name__, level=log_level)
    logger.info(grey + f"logging startet - re-writing of file: {ale_path}" + clrs)
    logger.info(grey + "Set 'log_level' to 'WARNING' or 'ERROR' to receive less logging output. "
                       "Set to 'CRITICAL' to receive no logging output" + clrs)
    # get current time
    curts = datetime.now().strftime("%H%M%S")

    # Extract the directory and filename from ale_path
    dir_path, filename = ale_path.rsplit("/", 1)

    # Check if the subfolder "altered_ale" exists in the directory, if not, create it
    subfolder_path = dir_path + "/altered_ale"
    subprocess.run(['mkdir', '-p', subfolder_path])

    # Split the filename into name and extension
    filename_parts = filename.rsplit(".", 1)
    new_filename = filename_parts[0] + "_new_" + curts
    logger.info(grey + f"new filename: {new_filename}" + clrs)

    if len(filename_parts) > 1:
        new_filename += "." + filename_parts[1]

    # Combine the subfolder path and the new filename to get the new file path
    new_ale_path = subfolder_path + "/" + new_filename
    logger.info(grey + f"new filepath: {new_ale_path}" + clrs)

    with open(new_ale_path, 'w', encoding=encoding, newline=newline) as ale:
        logger.info(grey + f"Writing new ALE file: {new_ale_path}" + clrs)
        # replace '\r\n' with '\n' in headerdict if newline is '\n'
        if newline == '\n':
            logger.debug(grey + str(headerdict) + clrs)
            logger.debug(grey + "Replacing '\\r\\n' with '\\n' in headerdict" + clrs)
            for key in headerdict:
                headerdict[key] = headerdict[key].replace('\r\n', '\n')
                logger.debug(grey + str(headerdict) + clrs)

        # Write headerdict excluding last line
        logger.info(grey + "Writing headerdict" + clrs)
        for key in headerdict:
            # write headerdict until "Column" line
            ale.write(headerdict[key])
            if "Column" in headerdict[key]:
                break

        # Write column names of dataframe
        logger.info(grey + "Writing column names of dataframe" + clrs)
        ale.write(delim.join(dataframe.columns) + "\n")

        # Write "Data" line
        logger.info(grey + "Writing Blank line and 'Data' line" + clrs)
        ale.write("\n")
        ale.write("Data\n")

        # Write content of dataframe excluding column names
        logger.info(grey + "Writing dataframe content" + clrs)
        dataframe.to_csv(ale, sep=delim, index=False, header=False, lineterminator=newline, encoding=encoding)

        # Return the new file credentials
        logger.info(grey + "Returning new file credentials" + clrs)
        return {
            'subfolder_path': subfolder_path,
            'new_filename': new_filename,
            'new_ale_path': new_ale_path
        }
