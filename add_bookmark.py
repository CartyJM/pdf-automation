
pdf_file = "恶魔法则.pdf"

import PyPDF2, re
from tqdm import tqdm 

# Function to count Chinese characters in a string
def count_chinese_characters(text):
    # Regular expression to match Chinese characters
    chinese_char_pattern = r'[\u4e00-\u9fff]'
    return len(re.findall(chinese_char_pattern, text))

# Function to extract bookmark name from text
def extract_bookmark_name(text):
    # Regular expression to find text between "第" and "章"
    pattern = r'第.*?章'
    match = re.search(pattern, text)


    if match and count_chinese_characters(match.group()) < 10:
        return match.group()
    return None

# Function to add bookmarks to a PDF when specific characters are found
def add_chapter_bookmarks(input_pdf, output_pdf):
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Iterate through each page in the PDF
        for i, page in tqdm(enumerate(reader.pages)):
            writer.add_page(page)

            # Extract text from the page
            page_text = page.extract_text()

            # Attempt to extract a bookmark name using the defined pattern
            bookmark_name = extract_bookmark_name(page_text)

            # If a bookmark name was extracted, add it as a bookmark
            if bookmark_name:
                writer.add_outline_item(title=bookmark_name, page_number=i)

        # Write the modified content to a new PDF file
        with open(output_pdf, 'wb') as new_file:
            writer.write(new_file)

# Usage
input_pdf = pdf_file # Replace with your PDF file path
output_pdf = 'output_with_bookmarks.pdf'

add_chapter_bookmarks(input_pdf, output_pdf)
