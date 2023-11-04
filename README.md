
# ALE (Avid Log Exchange) Parser

This script parses ALE (Avid Log Exchange) files and allows for the reading and writing of these files using pandas dataframes. It can read an ALE file into a pandas dataframe and a header dictionary, and can write a pandas dataframe and a header dictionary back to an ALE file. It also validates the ALE file format during reading and writing operations.

## Dependencies

- pandas
- printme (custom - included in this repository)
- colorama


To install these dependencies, use the following command:


`pip install pandas`
`pip install colorama`

## Usage



### Function 1: ale_read_parser

#### Description

Reads an ALE file and splits it into a header dictionary and a pandas dataframe.

#### Syntax

`
ale_read_parser(ale_file)
`

#### Parameters

- `ale_file`: The file path of the ALE file to read.

#### Return Value

- delim, headerdict, dataframe, ale_file = ale_read_parser(ale_path)

Returns a tuple containing
- delimiter type
- header dictionary (not to be mistaken with the column-header)
- pandas dataframe
- file path of the ALE file (as input parameter for the 2nd Function)

### Function 2: ale_write_parser

#### Description

Writes a pandas dataframe and a header dictionary to an ALE file.

#### Syntax

`
ale_rewrite(ale_path, delim, headerdict, dataframe)
`

#### Parameters

- `dataframe`: The pandas dataframe to write to the ALE file.
- `headerdict`: The header dictionary to write to the ALE file.
- `ale_path`: The file path and name where the ALE file will be saved.
- `delim`: The delimiter type of the ALE file.

## Error Handling

The script includes error handling to validate the format of the ALE file during both reading and writing operations. If an invalid format is detected, it will print an error message and exit the script.

## Example Usage

```python
# Path to the ALE file

from ALE_Parser import ale_read_parser, ale_rewrite
import printme

file = "your_ale_path.ale"

print("executing ale_read_parser")
delim, headerdict, dataframe, ale_file = (ale_read_parser(file)) # get main variables from read in function:

print("Returns from ale_read_parser:")
printme(delim)
printme(headerdict)
printme(dataframe)
printme(ale_file)


# write new ale file
print("executing ale_rewrite")
ale_rewrite(ale_file, delim, headerdict, dataframe)
```

This script demonstrates how to read an ALE file into a header dictionary and a pandas dataframe, and then write this data back to a new ALE file.

## Known Issues

- The script does not currently support the reading and writing of ALE files with multiple tables.

