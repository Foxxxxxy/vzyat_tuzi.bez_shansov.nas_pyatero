import json
import os

from fpdf import FPDF
from pypdf import PdfMerger, PdfReader

from app.src.pieces.calculation.schemas import CalculationPreparedDataSchema

script_dir = os.path.dirname(os.path.realpath(__file__))


class PdfCreator:

    def __init__(self, calculation_report: CalculationPreparedDataSchema, req_id: int):
        # Common data
        self.calculation_report = calculation_report

        self.util_files_dir = f"{script_dir}/utility_files"
        self.output_dir = f"{script_dir}/brochures"
        self.constructed_pdf_name = f"{self.util_files_dir}/constructed.pdf"
        self.output_pdf_name = f"{self.output_dir}/brochure{req_id}.pdf"
        with open(f"{self.util_files_dir}/pdf_structure_config.json") as config_file:
            self.pdf_config = json.load(config_file)

        self.constructed_pages = ["business_info_page",
                                  "employee_page"]
        self.pdfs_to_merge = [f"{self.util_files_dir}/title.pdf",
                              f"{self.util_files_dir}/greetings.pdf",
                              f"{self.util_files_dir}/constructed.pdf"]

        # pdf utils
        self.constructed_pdf = FPDF()
        self.pdf_merger = PdfMerger()

        # pdf settings
        self.__set_font_for_russian_language()

        # construction logic
        self.__construct_pdf(self.constructed_pdf_name)
        self.__merge_pdf_pages_to_pdf_file(self.output_pdf_name)

    def get_output_pdf_filename(self):
        return self.output_pdf_name

    def __merge_pdf_pages_to_pdf_file(self, output_pdf_name):
        for pdf_name in self.pdfs_to_merge:
            self.pdf_merger.append(PdfReader(open(pdf_name, 'rb')))
        self.pdf_merger.write(output_pdf_name)

    # Entry point for whole pdf construction
    def __construct_pdf(self, pdf_name):
        for page_name in self.constructed_pages:
            self.__construct_page(page_name)

        self.constructed_pdf.output(pdf_name)

    # Entry point for pages construction
    def __construct_page(self, page_name):
        page_config = self.pdf_config[page_name]

        self.constructed_pdf.add_page()
        for table_config in page_config["tables"]:
            self.__construct_table_for_page(table_config)

    def __construct_table_for_page(self, table_config):
        self.constructed_pdf.multi_cell(0, txt=table_config["table_name"])
        with self.constructed_pdf.table(first_row_as_headings=False) as table:
            for k, v in table_config["fields"].items():
                row = table.row()
                row_value = getattr(self.calculation_report, k)
                row.cell(str(v))
                row.cell(str(row_value))
        self.constructed_pdf.ln()

    def __set_font_for_russian_language(self):
        self.constructed_pdf.add_font(fname=f'{self.util_files_dir}/DejaVuSansCondensed.ttf')
        self.constructed_pdf.set_font('DejaVuSansCondensed', size=14)
