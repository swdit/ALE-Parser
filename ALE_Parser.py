#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ALE (Avid Log Exchange) Parser
Generates pandas data Frame from ALE file that can be treated like a usual tab delimited csv file.
Writes pandas dataframe to ALE file retattaching the ALE header.
"""


import pandas as pd



# Path to ALE file <- Change this to your ALE file
ale_path = "your_ale_path.ale"

# FUNCTION 1: Read ALE file into pandas dataframe and headerdict
def ale_read_parser(ale_file): #provide file (filepath) of the ale file as argument
    # ale_read_parser will split the ALE file into a dict containing the header + line-index and a pandas dataframe containing the data
    if not ale_file.split(".")[-1] == "ale":
        print(f"Error reading file {ale_file} - This is not a valid ALE-File")
        exit()
    def ale_parser_headerlines(ale_file):
        headerdict = {}
        # Dataframe-1: open ale and write lines 1,2,3,4,5,6,7,9, into dict
        with open(ale_file, 'r') as ale:
            line1_heading = ale.readline()
            # print(line1_heading, type(line1_heading))
            if line1_heading != "Heading\n":
                print(f"Error reading Heading on index 0 is {line1_heading} - This is not a valid ALE-File")
                exit()
            headerdict[0] = line1_heading # add line1_heading with line index as key to dict

            line2_delim = ale.readline()
            # print(line2_delim)
            if "FIELD_DELIM" not in line2_delim:
                print(f"Error reading FIELD_DELIM on index 1 is {line2_delim} - This is not a valid ALE-File")
                exit()
            headerdict[1] = line2_delim # add line2_delim with line index as key to dict

            line3_videoform = ale.readline()
            # print(line3_videoform)
            if "VIDEO_FORMAT" not in line3_videoform:
                print(f"Error reading VIDEO_FORMAT on index 2 is {line3_videoform} - This is not a valid ALE-File")
                exit()
            headerdict[2] = line3_videoform # add line3_videoform with line index as key to dict

            line4_audioform = ale.readline()
            #print(line4_audioform)
            if  "AUDIO_FORMAT" not in line4_audioform:
                print(f"Error reading AUDIO_FORMAT on index 3 is {line4_audioform} - This is not a valid ALE-File")
                exit()
            headerdict[3] = line4_audioform # add line4_audioform with line index as key to dict

            line5_fps = ale.readline()
            #print(line5_fps)
            if "FPS" not in line5_fps:
                print(f"Error reading FPS on index 4 is {line5_fps} - This is not a valid ALE-File")
                exit()
            headerdict[4] = line5_fps # add line5_fps with line index as key to dict

            line6_empty = ale.readline()
            #print(line6_empty)
            if line6_empty != "\n":
                print(f"Error reading empty line on index 5 is {line6_empty} - This is not a valid ALE-File")
                exit()
            headerdict[5] = line6_empty # add line6_empty with line index as key to dict

            line7_column = ale.readline()
            #print(line7_column)
            if line7_column != "Column\n":
                print(f"Error reading Column on index 6 is {line7_column} - This is not a valid ALE-File")
                exit()
            headerdict[6] = line7_column # add line7_column with line index as key to dict

            line8_header = ale.readline()
            #print(line8)
            if not line8_header.startswith("Name"):
                print(f"Error reading Header on index 7 is {line8_header} - This is not a valid ALE-File")
                exit()
            headerdict[7] = line8_header # add line8_header with line index as key to dict

            line9_empty = ale.readline()
            #print(line9_empty)
            if line9_empty != "\n":
                print(f"Error reading empty line on index 8 is {line9_empty} - This is not a valid ALE-File")
                exit()
            headerdict[8] = line9_empty # add line9_empty with line index as key to dict

            line10_data = ale.readline()
            #print(line10_data)
            if line10_data != "Data\n":
                print(f"Error reading Data on index 9 is {line10_data} - This is not a valid ALE-File")
                exit()
            headerdict[9] = line10_data # add line10_data with line index as key to dict


            # Return ALE-header Lines and Pandas Dataframe
            return headerdict


    def ale_parser_data(ale_file):
        # Read in Pandas-Dataframe from ALE; Headers in Line 8, Data beginning in Line 11, Delimiter is Tab, skip Lines 1,2,3,4,5,6,7,9,10
        skiprows = [0, 1, 2, 3, 4, 5, 6, 8, 9]
        df = pd.read_csv(ale_file, sep='\t', skiprows=skiprows, dtype=str) # dtype=str to prevent pandas from converting numbers to float
        df.head()
        return df

    headerdict = ale_parser_headerlines(ale_file)
    df = ale_parser_data(ale_file)

    return headerdict, df



# FUNCTION 2: Write ALE file from pandas dataframe and headerdict
def ale_write_parser(df, headerdict, save_path_and_name):
    # write df to file
    with open(save_path_and_name, 'w') as ale:
        # split pandas df into headerline and content
        df_header, df_content = df.iloc[:1], df.iloc[1:]
        # write headerdict to file
        for i in range(0, 10):
            ale.write(headerdict[i])
        # write headerline to file
        ale.write(df_header.to_csv(sep='\t', index=False, header=False))
        ale.write(df_content.to_csv(sep='\t', index=False, header=False))
    # check_ale
    try:
        # ReExecute ale_read_parser on newly created ALE file to check if it is valid
        ale_read_parser(save_path_and_name)
    except:
        print(f"Error writing ALE file to {save_path_and_name}")
        exit()









