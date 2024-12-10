"""
    Simple XML-JSON Parser

    This script provides a few functions for parsing and displaying info from
    XML files. It expects to be operating on well-formed .xml files.

    The following functions are provided:
        print_objects:  simply uses print() functions to show the info of a 
            specified object tag.
        
        dump_objects:   behaves similarly, but returns a JSON string of the
            specified object tag's contents.
"""

from json import dumps
from pathlib import Path
import xml.etree.ElementTree as ET

from defusedxml.ElementTree import parse

#### API Functions ####

def dump_objects(xml_to_parse: Path, object_to_print: str) -> str:
    """
        Iterate through an XML file and save its info to a new object.

        Returns a JSON string of the requested data.

        Keyword arguments:
        xml_to_parse -- filepath to the .xml file to parse, as a pathlib.Path.
        object_to_print -- string to represent the tag to search for.
    """

    if _is_xml_valid(xml_to_parse):

        root = _get_parsed_root(xml_to_parse)

        object_dict = []

        for element in root.iter(object_to_print):
            element_dict = _dump_object(element)
            object_dict.append(element_dict)

        return dumps(object_dict)

def print_objects(xml_to_parse: Path, object_to_print: str) -> None:
    """
        Iterate through an XML file and print the info of objects contained
        within.

        Keyword arguments:
        xml_to_parse -- filepath to the .xml file to parse, as a pathlib.Path.
        object_to_print -- string to represent the tag to search for.
    """

    if _is_xml_valid(xml_to_parse):

        root = _get_parsed_root(xml_to_parse)

        for element in root.iter(object_to_print):
            _print_object(element)

            # Add a cosmetic newline
            print()

#### Internal Functions ####

def _dump_object(element: ET.Element):
    """
        Iterate through an element and save its properties to a dictionary.
        This function doesn't perform the JSON dump itself; it just helps to
        assemble a dictionary. Performs recursion if it encounters nested
        elements.

        Returns a dict containing the element contents.

        Keyword arguments:
        element -- the ET.Element object to iterate through.
    """
    element_dict = {}
    for entry in element:
        # If the tag has its own children, work recursively.
        if len(entry) > 0:
            element_dict[entry.tag] = _dump_object(entry)
        else:
            element_dict[entry.tag] = entry.text
    return element_dict

def _get_longest_tag_length(element: ET.Element) -> int:
    """
        Get the length of the longest tag name in the given element. This is
        intended for use alongside print_object() for a proper display of the
        tag names and their text.

        Returns an int that represents the length of the longest tag name.

        Keyword arguments:
        element -- an ET.Element to measure tag length.
    """

    longest_tag_length = 0
    for entry in element:
        longest_tag_length = max(len(entry.tag), longest_tag_length)
    return longest_tag_length

def _get_parsed_root(xml_to_parse: Path) -> ET.Element:
    """
        Return a defusedxml root as an ET.Element object. defusedxml is used
        to avoid XML vulnerabilities. 
        (https://docs.python.org/3/library/xml.html#xml-vulnerabilities)

        Make sure to validate beforehand with is_xml_valid()! This
        function assumes that the XML file is valid.

        Keyword arguments:
        xml_to_parse -- filepath to the .xml file to parse, as a pathlib.Path.
    """

    # Utilize defusedxml's parse override for safe parsing.
    tree = parse(xml_to_parse)
    return tree.getroot()

def _is_xml_valid(xml_to_parse: Path) -> bool:
    """
        Utilizes pathlib to confirm that the given XML file exists, is a file,
        and has a .xml suffix.
        
        Returns True or False if the file is valid.

        Keyword arguments:
        xml_to_parse -- filepath to the .xml file to parse, as a pathlib.Path.
    """

    path = Path(xml_to_parse)
    if path.exists():
        if path.is_file():
            if path.suffix == ".xml":
                return True
    return False

def _print_object(element: ET.Element, depth=0) -> None:
    """
        Try to nicely display the text of all of the element's entries,
        recursively.

        Keyword arguments:
        element -- the element whose properties must be iterated over.
        depth -- used for recursion. Equal to the number of tabs to insert. 
    """
    longest_tag_length = _get_longest_tag_length(element)
    for entry in element:
        # If the tag has its own children, print recursively.
        if len(entry) > 0:
            print(entry.tag + ":")
            _print_object(entry, depth + 1)
        else:
            tabs = "\t" * depth
            tag = (tabs + entry.tag + ":").ljust(longest_tag_length + 1)
            print(f"{tag} {entry.text}")

if __name__ == "__main__":
    # NOTE: Purely a demo; invoking this script directly is not intended use.
    print_objects("plant_catalog.xml", "PLANT")
