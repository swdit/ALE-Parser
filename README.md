
# ALE (Avid Log Exchange) Parser

This script parses ALE (Avid Log Exchange) files and allows for the reading and writing of these files using pandas dataframes. It can read an ALE file into a pandas dataframe and a header dictionary, and can write a pandas dataframe and a header dictionary back to an ALE file. It also validates the ALE file format during reading and writing operations.

## Dependencies

- pandas


To install these dependencies, use the following command:

\```bash
pip install pandas
\```

## Usage

### Setting up the ALE File Path

Set up the path to your ALE file by modifying the `ale_path` variable:

\```python
ale_path = "your_ale_path.ale"
\```

### Function 1: ale_read_parser

#### Description

Reads an ALE file and splits it into a header dictionary and a pandas dataframe.

#### Syntax

\```python
ale_read_parser(ale_file)
\```

#### Parameters

- `ale_file`: The file path of the ALE file to read.

#### Return Value

Returns a tuple containing the header dictionary and the pandas dataframe.

### Function 2: ale_write_parser

#### Description

Writes a pandas dataframe and a header dictionary to an ALE file.

#### Syntax

\```python
ale_write_parser(df, headerdict, save_path_and_name)
\```

#### Parameters

- `df`: The pandas dataframe to write to the ALE file.
- `headerdict`: The header dictionary to write to the ALE file.
- `save_path_and_name`: The file path and name where the ALE file will be saved.

## Error Handling

The script includes error handling to validate the format of the ALE file during both reading and writing operations. If an invalid format is detected, it will print an error message and exit the script.

## Example Usage

\```python
# Path to the ALE file
ale_path = "your_ale_path.ale"

# Read the ALE file
headerdict, df = ale_read_parser(ale_path)

# Define the save path and name
save_path_and_name = "path_to_save.ale"

# Write the data to a new ALE file
ale_write_parser(df, headerdict, save_path_and_name)
\```

This script demonstrates how to read an ALE file into a header dictionary and a pandas dataframe, and then write this data back to a new ALE file.
