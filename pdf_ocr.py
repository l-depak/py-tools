'''
Prerequisite:
1. brew install tesseract
2. pip install pytesseract pdf2image pillow
3. Download trained files from https://github.com/tesseract-ocr/tessdata
4. Copy "*.traineddata" files to /usr/local/Cellar/tesseract/<version>/share/tessdata
'''

# Credit to https://www.geeksforgeeks.org/python-reading-contents-of-pdf-using-ocr-optical-character-recognition/

import argparse
from tempfile import TemporaryDirectory
from pathlib import Path

import pytesseract
from pdf2image import convert_from_path
from PIL import Image


def pdf_ocr(input_file, input_lang):

    image_file_list = []

    # Name of the output text file.
    text_file = Path(input_file).with_suffix('.txt')

    # Create a temporary directory to hold our temporary images.
    with TemporaryDirectory() as tempdir:

        """
        Part 1 : Converting PDF to images
        """
        # Read in the PDF file at 500 DPI
        pdf_pages = convert_from_path(input_file, 500)

        # Iterate through all the pages stored above
        for page_enumeration, page in enumerate(pdf_pages, start=1):

            # Create a file name to store the image
            image_filename = f"{tempdir}\page_{page_enumeration:03}.jpg"

            # Declaring filename for each page of PDF as JPG, e.g.:
            # PDF page 1 -> page_001.jpg
            # PDF page 2 -> page_002.jpg
            # ....
            # PDF page n -> page_00n.jpg

            # Save the image of the page in system
            page.save(image_filename, "JPEG")
            image_file_list.append(image_filename)

        """
        Part 2 : Recognizing text from the images using OCR
        """
        with open(text_file, "a") as output_file:
            # Open the file in append mode so that
            # All contents of all images are added to the same file

            # Iterate from 1 to total number of pages
            for image_file in image_file_list:

                # Recognize the text as string in image using pytesserct
                text = str((pytesseract.image_to_string(Image.open(image_file), lang=input_lang)))

                # Remove 'hyphen' for the last word in a line by replacing every '-\n' to ''.
                text = text.replace("-\n", "")

                # Write the processed text to the file.
                output_file.write(text)

        # At the end of the with .. tempdir block, the
        # TemporaryDirectory() we're using gets removed.


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='PDF OCR.')
    parser.add_argument('filename', help='Input the file name.')
    parser.add_argument('-l', '--lang', default='eng', choices=['eng', 'chi_tra', 'chi_tra_vert', 'chi_sim', 'chi_sim_vert'])
    args = parser.parse_args()

    pdf_ocr(args.filename, args.lang)
