"""Information Structure Final Project."""


import pprint
import json
from collections import OrderedDict

# pp = pprint.PrettyPrinter(indent=1)


def main():
    """Rund main application."""
    # Getting user input.
    file_name = input_file_name()
    # file_name = "sample_1.hl7"
    # Opening the file for read.
    open_hl7 = open_hl7_file(file_name)

    # Creates an array from each line of the file.
    # ["line0", "line1", "line2", "..."]
    file_array = file_to_array(open_hl7)

    # Creates each line of the array into its own array.
    # [["element1", "element2", "..."], ["element1", "element2", "..."], ...]
    # line_array = delete_char(file_array)
    line_array = array_of_lines(file_array)

    # Cleans the 'line_array' by deleting empty sting elements
    # [["MSH", "^~\\&", "", ""], ["PID", "1", "9081717170722.97472", ""]]
    clean_line_array = delete_empty_str(line_array)

    # Creates a 'OrderedDict()' out of the matrix array.
    hl7_dictionary = create_dictionary(clean_line_array)

    # pp.pprint(hl7_dictionary)
    # Writes the 'OrderedDict()' to a json file.
    to_json(hl7_dictionary)

    # print_to_console(hl7_dictionary)


def input_file_name():
    """
    Function ask the user for file name.

    :return: Path to file.
    """
    return input("Enter HL7 file name to be parsed: ")


def open_hl7_file(file):
    """
    Get the file's path and opens the file.

    :param file: A path to a file to be parsed.
    :return: The open file object.
    """
    return open(file, "r")


def file_to_array(file):
    """Take raw file and append to array."""
    file_array = []
    for text in file:
        file_array.append(text)
    return file_array


def array_of_lines(file_array):
    """
    Split elements by '|'.

    :param file_array: Array with lines of strings.
    :return: An array with elements without the '|'.
    """
    file_line_array = []
    for lines in file_array:
        file_line_array.append(lines.split("|"))
    line_with_str = delete_empty_str(file_line_array)
    return line_with_str


def delete_empty_str(file):
    r"""
    Delete elements with empty values from line_array.

    [["MSH", "^~\&", "", ""], ["PID", "1", "9081717170722.97472", ""]]
    :param file: Takes the array of lines.
    :return: An array of lines without empty elements
    """
    line_array = []
    for lines in file:
        line_with_str = [string for string in lines if string]
        line_array.append(line_with_str)
    return line_array


def delete_char(string):
    r"""
    Delete character from string (e.g. "^~\&").

    :param string: Take a string to be parsed.
    :return: Returns the string without the undesired character.
    """
    if "^" in string and string != r"^~\&":
        return string.split("^")
    elif "~" in string and string != r"^~\&":
        return string.split("~")
    else:
        return string


def create_dictionary(file):
    """
    Create a dictionary out of an array of hl7 lines.

    :param file: Takes an array obj.
    :return: Dictionary
    """
    line = OrderedDict()
    for key, each_line in enumerate(file):
        # Reset each sub_line on each iteration.
        sub_line = OrderedDict()
        # Sets the very outer key.
        top_key = each_line[0]
        # Iterates over the dictionary.
        for sub_key, value in enumerate(each_line):
            # Reset third level of dictionary where split ("|").
            sub_sub_line = OrderedDict()
            sub_line[top_key + "." + str(sub_key)] = value.replace("\n", "")
        for sub_sub_k, sub_sub_v in sub_line.items():
            # Reset third level of dictionary where split ("^", "~").
            last_line = OrderedDict()
            # Split sub level by "^" and "~".
            value = delete_char(sub_sub_v)
            # Delete empty positions from split array.
            if isinstance(value, list):
                sub_array = [string for string in value if string]
                # Creating sub-dictionary for elements "^" and "~".
                for k, item in enumerate(sub_array):
                    last_line[sub_sub_k + "." + str(k)] = item
                    value = last_line
            # Append to dictionary.
            line_with_str = value
            # Delete empty positions from split outter array.
            if isinstance(line_with_str, list):
                sub_sub_line[sub_sub_k] = [
                    string for string in line_with_str if string]
            else:
                sub_sub_line[sub_sub_k] = line_with_str
        # Creating sub dictionary.
        sub_line = sub_sub_line

        # Add sub_line to the dictionary.
        line[top_key] = sub_line
    return line


def to_json(dict_obj):
    """
    Write a json file from the input data.

    :param dict_obj: OrderedDict() object
    :return: Writes a json file.
    """
    with open("data.json", "w") as out_file:
        json.dump(dict_obj, out_file, indent=4)


def print_to_console(dict_obj):
    """Print beautify jason."""
    pp = pprint.PrettyPrinter(indent=1)
    pp.pprint(dict_obj)


if __name__ == '__main__':
    main()
