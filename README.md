
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
ale_path = "your_ale_path.ale"

# Read the ALE file
headerdict, df = ale_read_parser(ale_path)

# alter the dataframe here
df = df.drop(df.index[3, 4, 5])

# Define the save path and name
save_path_and_name = "path_to_save.ale"

# Write the data to a new ALE file
ale_write_parser(df, headerdict, save_path_and_name)
```

This script demonstrates how to read an ALE file into a header dictionary and a pandas dataframe, and then write this data back to a new ALE file.

## Known Issues

1. Pandas might interpret numbers as floats and write them back with dot zero.
`Take 1 -> Take 1.0`

2. If the ALE Header does not contain "AUDIO_FORMAT" on index 3 the ALE is treated as invalid an the script will stop.

