#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALE (Avid Log Exchange) Parser
Generates pandas data Frame from ALE file that can be treated like a usual tab delimited csv file.
Writes pandas dataframe to ALE file reattaching the ALE header.

Parse ALEs:
Reader:
- find all Lines that start with only two columns (headerdict)
- check for delimiter
- remember line number
- make sure everything is being read as string (no int, no float)

Writer:
- write headerdict (lines with only two columns)
- write column names of dataframe
- write "Data" line
- write content of dataframe excluding column names
"""

from datetime import datetime
import pandas as pd
import subprocess




# FUNCTION 1: Read ALE file into pandas dataframe and headerdict
def ale_read_parser(ale_file): #provide file (filepath) of the ale file as argument
    if not ale_file.split(".")[-1] == "ale":
        print(f"Error reading file {ale_file} - This is not a valid ALE-File")
        exit()
    with open (ale_file, 'r') as ale: # First Read of the Original ALE and Check for Delimiter Status
        firstline = ale.readline()
        scndline = ale.readline()
        if not "Heading" in firstline:
            if "COMMAS" in firstline:
                delim = ","
                print ("This is a comma separated ALE file")
            elif "TABS" in firstline:
                delim = "\t"
                print ("This is a tab separated ALE file")
            else:
                print ("@DELIM - This is not a valid ALE file")
                print (firstline)
                exit()
        elif "Heading" in firstline:
            if "COMMAS" in scndline:
                delim = ","
                print ("This is a comma separated ALE file")
            elif "TABS" in scndline:
                delim = "\t"
                print ("This is a tab separated ALE file")
            else:
                print ("@DELIM - This is not a valid ALE file")
                print (firstline)
                exit()
        else:
            print (f"Firstline-Error - This is not a valid ALE file")
            print ("firstline", firstline, "scndline", scndline)
            exit()



    def ale_parser_headerlines(ale_file_infu):
        headerdict_infu = {}
        skiprows_infu = []
        headskip = False
        with open(ale_file_infu, 'r') as ale_infu: # 2nd Read of Original ALE and to red the Headerlines
            for idx, line in enumerate(ale_infu):
                # if headskip is False, check for header lines (needed to skip Column-Names as those shall end up in the data frame)
                if not headskip:
                    # add idx and line to headerdict
                    headerdict_infu[idx] = line
                    # add idx to skiprows list
                    skiprows_infu.append(idx)
                headskip = False
                if "Column" in line:
                    headskip = True
                if "Data" in line: # if "Data" is in line, stop reading header lines
                    break


        return headerdict_infu, skiprows_infu

    def getdataframe(ale_file_int, delim_infu):
        df = pd.read_csv(ale_file_int, delimiter=delim_infu, skiprows=skiprows)
        return df


    headerdict, skiprows = ale_parser_headerlines(ale_file) # execute funktion for delimiter and headerlines
    dataframe = getdataframe(ale_file, delim) # execute funktion for main dataframe
    return delim, headerdict, dataframe, ale_file

# FUNCTION 2: Write pandas dataframe to ALE file reattaching the ALE header.
def ale_rewrite(ale_path, delim, headerdict, dataframe):
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

    if len(filename_parts) > 1:
        new_filename += "." + filename_parts[1]

    # Combine the subfolder path and the new filename to get the new file path
    new_ale_path = subfolder_path + "/" + new_filename

    with open(new_ale_path, 'w') as ale:
        # Write headerdict excluding last line
        for key in headerdict:
            ale.write(headerdict[key])
            if "Column" in headerdict[key]:
                break

        # Write column names of dataframe
        ale.write(delim.join(dataframe.columns) + "\n")

        # Write "Data" line
        ale.write("\n")
        ale.write("Data\n")


        # Write content of dataframe excluding column names
        dataframe.to_csv(ale, sep=delim, index=False, header=False)








