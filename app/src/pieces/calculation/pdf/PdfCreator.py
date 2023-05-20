from typing import Dict

from fpdf import FPDF


class Report:
    def __init__(self, data: Dict):
        self.data = data

    def get_data(self):
        return self.data


class PdfCreator:

    def __init__(self, report: Report):
        self.report = report

        self.pdf = FPDF()
        self.__set_font_for_russian_language()

        self.__add_table_with_calculation_data()

    def output_pdf(self, pdf_name):
        self.pdf.output(pdf_name)

    def __set_font_for_russian_language(self):
        self.pdf.add_font(fname='DejaVuSansCondensed.ttf')
        self.pdf.set_font('DejaVuSansCondensed', size=14)

    def __add_table_with_calculation_data(self):
        self.pdf.add_page()
        with self.pdf.table(first_row_as_headings=False) as table:
            for k, v in self.report.get_data().items():
                row = table.row()
                row.cell(k)
                row.cell(v)


def main():
    report = Report(
        {"1": "1", "2": "2", "3": "3"}
    )
    pdf_creator = PdfCreator(report)
    pdf_creator.output_pdf("brochure.pdf")


if __name__ == "__main__":
    main()
