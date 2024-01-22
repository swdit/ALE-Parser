
# ALE (Avid Log Exchange) Parser

This script parses ALE (Avid Log Exchange) files and allows for the reading and writing of these files using pandas dataframes. 

It can read an ALE file into a pandas dataframe and a header dictionary, and can write a pandas dataframe and a header dictionary back to an ALE file. 

It also validates the ALE file format during reading operations and can display warnings and errors if the ALE file format is invalid.




## Dependencies

- pandas
- chardet
- colorama
- printme (custom - included in this repository)
- swdit_logger (custom - included in this repository)


To install these dependencies, use the following commands or use the requirements.txt file:


`pip install pandas`
`pip install colorama`
`pip install chardet`


## Usage



### Function 1: ale_read_parser

#### Description

Reads an ALE file and splits it into a header dictionary and a pandas dataframe (and some advanced stuff).

#### Syntax

`
ale_read_parser(ale_file, log_level = INFO)
`

log_level is an optional parameter.

#### Parameters

- `ale_file`: The file path of the ALE file to read.
- `log_level`: The log level to use for the logger. Default is INFO. Options are INFO, DEBUG, WARNING, ERROR, CRITICAL. CRITICAL will print no log messages.

#### Return Value

- delim, headerdict, dataframe, ale_file, encoding = ale_read_parser(ale_path, log_level = INFO)

Returns a tuple containing
- delimiter type
- header dictionary (not to be mistaken with the column-header)
- pandas dataframe
- file path of the ALE file (as input parameter for the 2nd Function)
- encoding of the ALE file (optional)

### Function 2: ale_write_parser

#### Description

Writes a pandas dataframe and a header dictionary to an ALE file.

#### Syntax

`
ale_rewrite(ale_path, delim, headerdict, dataframe, encoding = None, newline = None, log_level = INFO)
`

encoding and newline are optional parameters.

#### Parameters

- `dataframe`: The pandas dataframe to write to the ALE file.
- `headerdict`: The header dictionary to write to the ALE file.
- `ale_path`: The file path and name where the ALE file will be saved.
- `delim`: The delimiter type of the ALE file.
- `encoding`: The encoding of the ALE file. Default is None, which will use the default encoding of the system.
- `newline`: The newline character to use when writing the ALE file. Default is None, which will use the default newline character is LF coded as `'/n'`.

## Error Handling

The script includes error handling to validate the format of the ALE file during both reading and writing operations. If an invalid format is detected, it will log an error message and exit the script.
The Script also includes a logger to log the progress of the script. The logger can be configured to log messages of different levels. The default log level is INFO, which will log all messages of level INFO and above. The logger can be configured to log messages of level DEBUG, INFO, WARNING, ERROR, and CRITICAL. CRITICAL will log no messages.
Warning messages usually show issues that might affect the output of the script, but the script will continue to run. Error messages usually show issues that will affect the compatibility of the ALE with Avid-Media Composer but do not affect the output of the script. 

## Example Usage

```python
# Path to the ALE file

from ALE_Parser import ale_read_parser, ale_rewrite
from printme import printme

file = "your_ale_path.ale"

print("executing ale_read_parser")
# get main variables from read in function:
delim, headerdict, dataframe, ale_file, encoding = (ale_read_parser(file, log_level='INFO')) 

print("Returns from ale_read_parser:")
printme(delim)
printme(headerdict)
printme(dataframe)
printme(ale_file)
printme(encoding)  # optional


# write new ale file
print("executing ale_rewrite")
# write main variables into new ale file (encoding and newline are optional):
ale_rewrite(ale_file, delim, headerdict, dataframe, encoding, newline=None, log_level='INFO')
```

This script demonstrates how to read an ALE file into a header dictionary and a pandas dataframe, and then write this data back to a new ALE file.

## Known Issues

- The script does not currently support the reading and writing of ALE files with multiple tables.
- The Script does not support deprecated CR character as newline character. 
- The script does currently no offer the option to fix Avid-Media Composer compatibility issues. This will be added in a future version.

