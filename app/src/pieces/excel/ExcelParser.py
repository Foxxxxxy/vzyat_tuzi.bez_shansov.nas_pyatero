from io import BytesIO
from tempfile import SpooledTemporaryFile

import openpyxl


class ExcelParser:

    def __init__(self, excel_file: SpooledTemporaryFile):
        book = openpyxl.load_workbook(filename=BytesIO(excel_file.read()))
        sh = book.sheet_by_index(0)
        for rx in range(sh.nrows):
            print(sh.row(rx))


def main():
    book = openpyxl.load_workbook(filename="/Users/nikitakhaurov/Documents/Book1.xlsx")


if __name__ == "__main__":
    main()
