# HL7 Parsers

This is a basic hl7 parser that takes the `sample_1.hl7` file that is in the root. The script will parse the file and will create `json` representation and write the content in a file called `data.json`. If the `data.json` already exists in the root directory, delete the file.

1. To run the script open the terminal and `cd` to the directory you clone the repo.
1. Make sure you delete the `data.json` file.
1. Run the command... `python parser.py`
1. The app will prompt to enter the file name to parse...
1. Enter the file name `sample_1.hl7`.
1. Open the `data.json` that got created.