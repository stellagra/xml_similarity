from xml_similarity import get_xml_similarity

# Provide the file paths of the XML files to compare
file1 = 'file1.xml'
file2 = 'file2.xml'

# Call the compare_xml_files function if providing the same file
similarity = get_xml_similarity(file1, file1)
print(f"Similarity ratio (including empty elements): {similarity}")

# Call the compare_xml_files function if providing different files
similarity = get_xml_similarity(file1, file2)
print(f"Similarity ratio (including empty elements): {similarity}")
