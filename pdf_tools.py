import os, glob, argparse
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger      # pip3 install pypdf2

'''
Merge multiple PDF files into a single PDF.
'''
def merger(output, input_path):
    pdf_merger = PdfFileMerger()
    files = []

    for path in input_path:
        pdf_merger.append(path)

    with open(output, 'wb') as fmerge:
        pdf_merger.write(fmerge)

'''
Split a PDF file by pages.
'''
def splitter(output, input_path):
    if output:
        file_name = output
    else:
        file_name = os.path.splitext(os.path.basename(input_path))[0]

    pdf = PdfFileReader(input_path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))

        output_filename = '{}_page_{}.pdf'.format(file_name, page+1)

        with open(output_filename, 'wb') as fpage:
            pdf_writer.write(fpage)

        print('Created: {}'.format(output_filename))

'''
Main function
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Merge or split PDF files.')
    func_group = parser.add_mutually_exclusive_group(required=True)
    func_group.add_argument('-m', '--merge', help='Merge function.', action='store_true')
    func_group.add_argument('-s', '--split', help='Split function.', action='store_true')
    parser.add_argument('-o', '--output', help='<Optional for split function> Output filename.')
    parser.add_argument('-i', '--input', help='<Required> Input folder/file paths.', nargs='+', required=True)
    args = parser.parse_args()

    if args.merge:
        if not args.output:
            print('Please enter an output filename (e.g. "-o OUTPUT.pdf").')
        else:
            if len(args.input) > 1:
                merger(args.output, args.input)
            else:
                full_path = args.input[0] + '/*.pdf'
                input_paths = glob.glob(full_path)
                input_paths.sort()
                merger(args.output, input_paths)
    elif args.split:
        if len(args.input) > 1:
            print('Only split one PDF each time.')
        splitter(args.output, args.input[0])

