import xml.etree.ElementTree as ET
import re
import os

def get_xml_similarity(file1, file2, bool_verbose = False, mode=0):
    """
    Compare two XML files and calculate the similarity ratio.
    - ratio = 0   : 0 of the elements match
    - ratio = 0.5 : 50% of the elements from the file with more elements match the other file
    - ratio = 1   : all of the elements match, i.e. suggesting that the two input files re the same.

    input:
        file1 (str): Path to the first XML file.
        file2 (str): Path to the second XML file.

    output: 
        numerical value representing the similarity between the files, based on different modes
            - mode=0 : ratio of matching elements including empty elements
            - mode=1 : ratio of matching non-empty elements
    """
    # expand list of different modes 
    if mode==0: # if elements are empty (empty string, spaces, tabs, ...) = match
        bool_empty_is_match = True 
    if mode==1: # if elements are empty (empty string, spaces, tabs, ...) NOT a match
        bool_empty_is_match = False 

    # Check if input files exist and read files
    if not (os.path.isfile(file1)):
        print("- current directory "+os.getcwd())
        raise FileNotFoundError(f"file >{file1}< does not exist")
    if not (os.path.isfile(file2)):
        print("- current directory "+os.getcwd())
        raise FileNotFoundError(f"file >{file2}< does not exist")

    tree1 = ET.parse(file1)
    tree2 = ET.parse(file2)

    root1 = tree1.getroot()
    root2 = tree2.getroot()

    # count number of elements in files
    num_elements1 = count_elements(root1)
    num_elements2 = count_elements(root2)
    if bool_verbose:
        print(f"number of elements {num_elements1}, {num_elements2}")
    max_elements = max(num_elements1, num_elements2)

    # init counter
    match_count = 0
    counter = 0
    for elem1 in root1.iter():
        for elem2 in root2.iter():
            counter = counter+1
            if bool_verbose:
                print(f"============== counter comparisons {counter} ============== ")
                print("- investigating the elements")
                print("--- element 1 ---")
                print("-- tag ")
                print(elem1.tag)
                print("-- attrib ")
                print(elem1.attrib )
                print("-- text ")
                print(elem1.text)
                
                print("--- element 2 ---")
                print("-- tag ")
                print(elem2.tag)
                print("-- attrib ")
                print(elem2.attrib )
                print("-- text ")
                print(elem2.text)

            if elem1.tag == elem2.tag and elem1.attrib == elem2.attrib:
                if is_matching_text(elem1.text, elem2.text, bool_empty_is_match):
                    match_count += 1
                    if bool_verbose:
                        print(" => they match!")
                        print(">"+str(elem1.text)+"<")
                        print(">"+str(elem2.text)+"<")
                if bool_verbose:
                    print("----------")
                break  # Move to the next element in root1

    print(f"- {match_count} of {max_elements} elements match.\n- Total number of comparisons: {counter}")
    similarity_ratio = match_count / max_elements

    return similarity_ratio

def count_elements(element):
    count = 1  # Count the current element
    for child in element:
        count += count_elements(child)  # Recursively count child elements
    return count

def is_matching_text(text1, text2, bool_empty_is_match=False):
    if text1 is None:
        text1 = ""
    if text2 is None:
        text2 = ""
    if bool_empty_is_match:
        return text1 == text2
    else:
        text1 = normalize_text(text1)
        text2 = normalize_text(text2)
        return text1 == text2 and (text1.strip() != "" and text2.strip() != "")
        

def normalize_text(text):
    if text:
        # Remove leading/trailing whitespace, spaces, and newlines
        text = text.strip()
        # Remove consecutive spaces and newlines when there is no alphanumeric character
        text = re.sub(r'(?<![A-Za-z0-9])[\s\n]+(?![A-Za-z0-9])', '', text)
    return text
