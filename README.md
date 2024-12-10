# xml-json-parser-demo
A simple XML to JSON parser written in Python. It provides two API functions:
    dump_objects(xml_to_dump, object_tag)
    print_objects(xml_to_dump, object_tag)

Given a valid .xml file in xml_to_dump and an object_tag to search for, the
API will either return its contents as a JSON string or simply print them to
the console as requested.

Initial data sample (breakfast_menu.xml) was sourced from W3Schools 
(https://www.w3schools.com/xml/xml_examples.asp). Specifically, the three 
samples are the XML CD Catalog (https://www.w3schools.com/xml/cd_catalog.xml), 
the XML plant catalog (https://www.w3schools.com/xml/plant_catalog.xml), and a 
slightly modified XML food catalog (https://www.w3schools.com/xml/simple.xml).

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)