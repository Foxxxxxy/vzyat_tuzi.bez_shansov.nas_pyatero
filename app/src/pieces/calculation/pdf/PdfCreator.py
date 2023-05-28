import json
import os

from fpdf import FPDF, XPos, YPos
from pypdf import PdfMerger, PdfReader
import flatdict

from app.src.pieces.calculation.schemas import CalculationPreparedDataSchema

script_dir = os.path.dirname(os.path.realpath(__file__))


class PdfCreator:

    def __init__(self, calculation_report: CalculationPreparedDataSchema, req_id: int):
        # Common data
        self.calculation_report = calculation_report
        self.req_id = req_id

        self.util_files_dir = f"{script_dir}/utility_files"
        self.text_files_dir = f"{self.util_files_dir}/text_files"
        self.output_dir = f"{script_dir}/brochures"
        self.constructed_pdf_name = f"{self.output_dir}/constructed{req_id}.pdf"
        self.output_pdf_name = f"{self.output_dir}/brochure{req_id}.pdf"
        with open(f"{self.util_files_dir}/pdf_structure_config.json") as config_file:
            self.pdf_config = json.load(config_file)

        self.constructed_pages = ["business_info_page",
                                  "employee_page",
                                  "rent_page",
                                  "taxes_page",
                                  "accounting_services_page",
                                  "equipment_page",
                                  "buildings_page",
                                  "additional_services_page"]
        self.pdfs_to_merge = [f"{self.util_files_dir}/title.pdf",
                              f"{self.util_files_dir}/greetings.pdf",
                              f"{self.output_dir}/constructed{req_id}.pdf",]

        # pdf utils
        self.constructed_pdf = FPDF()
        self.pdf_merger = PdfMerger()

        # pdf settings
        self.__add_font_for_russian_language(self.constructed_pdf)
        self.__set_font_for_russian_language(self.constructed_pdf, 14)

        # construction logic
        self.constructed_files = []
        self.__construct_pdf(self.constructed_pdf_name)
        self.__merge_pdf_pages_to_pdf_file(self.output_pdf_name)

    def get_output_pdf_filename(self):
        return self.output_pdf_name

    def get_output_files_for_zip(self):
        return self.constructed_files

    def __merge_pdf_pages_to_pdf_file(self, output_pdf_name):
        for pdf_name in self.pdfs_to_merge:
            self.pdf_merger.append(PdfReader(open(pdf_name, 'rb')))
        self.pdf_merger.write(output_pdf_name)
        self.constructed_files.append(output_pdf_name)

    # Entry point for whole pdf construction
    def __construct_pdf(self, pdf_name):
        for page_name in self.constructed_pages:
            self.__construct_page(page_name)

        self.constructed_pdf.output(pdf_name)

    # Entry point for pages construction
    def __construct_page(self, page_name):
        page_config = self.pdf_config[page_name]

        # Background and lines
        self.constructed_pdf.add_page()
        self.constructed_pdf.image(f'{self.util_files_dir}/background.jpg', x=0, y=0, w=210,
                                   h=297, type='', link='')
        self.constructed_pdf.ln(23)

        self.__set_page_title(self.constructed_pdf, page_config["title"])

        for text_file in page_config["texts"]:
            self.__construct_text_for_page(self.constructed_pdf, text_file)

        for table_config in page_config["tables"]:
            self.__construct_table_for_page(self.constructed_pdf, table_config)

        for file_config in page_config["external_files"]:
            self.__construct_external_files_for_page(file_config)

    def __set_page_title(self, pdf_file: FPDF, heading):
        self.__set_font_for_russian_language(pdf_file, 30)
        pdf_file.multi_cell(w=190, txt=heading, align='CENTER', markdown=True)
        pdf_file.ln(5)
        self.__set_font_for_russian_language(pdf_file, 14)

    def __construct_text_for_page(self, pdf_file: FPDF, text_file_name):
        pdf_file.ln(2)
        with open(f"{self.text_files_dir}/{text_file_name}") as f:
            text = "\n".join(f.readlines())
            pdf_file.multi_cell(w=190, txt=text,
                                align='CENTER', print_sh=False,
                                max_line_height=pdf_file.font_size)
        pdf_file.ln(3)

    def __construct_table_for_page(self, pdf_file: FPDF, table_config, horizontal_table=False):
        pdf_file.ln(2)
        pdf_file.multi_cell(0, txt=table_config["table_name"], align='CENTER', markdown=True)
        pdf_file.ln(2)
        if not horizontal_table:
            with pdf_file.table(text_align='CENTER', width=150,
                                first_row_as_headings=False) as table:
                for k, v in table_config["fields"].items():
                    row = table.row()
                    row_value = str(getattr(self.calculation_report, k))
                    if str(k) in table_config["rub_fields"]:
                        row_value += ", руб."
                    row.cell(str(v))
                    row.cell(str(row_value))
        else:
            with pdf_file.table(text_align='CENTER', width=190,
                                first_row_as_headings=True) as table:
                data_source = self.__get_data_source_for_table(table_config["data_source_field"],
                                                               table_config["excluded_fields"])
                h_row = table.row()
                for h in table_config["headers"]:
                    h_row.cell(h)
                for d in data_source:
                    row = table.row()
                    for k, v in d.items():
                        if k == "id":
                            continue
                        row.cell(str(v))
        pdf_file.ln(2)

    def __construct_external_files_for_page(self, file_config):
        external_file = FPDF()
        self.__add_font_for_russian_language(external_file)
        self.__set_font_for_russian_language(external_file, 14)

        external_file.add_page()
        self.__set_page_title(external_file, file_config["title"])
        self.__construct_text_for_page(external_file, file_config["intro_text_file"])

        for table_config in file_config["tables"]:
            self.__construct_table_for_page(external_file, table_config, horizontal_table=True)

        filename = f"{self.output_dir}/{file_config['filename']}{self.req_id}.pdf"

        external_file.output(filename)
        self.constructed_files.append(filename)

    def __get_data_source_for_table(self, data_source_field, excluded_fields):
        data_source_list = getattr(self.calculation_report, data_source_field)
        data_source = [flatdict.FlatDict(it.dict()) for it in data_source_list]

        for it in data_source:
            for excluded_field in excluded_fields:
                del it[excluded_field]
        return data_source

    def __add_font_for_russian_language(self, pdf_file: FPDF):
        pdf_file.add_font("Golos", "", f'{self.util_files_dir}/golos-text_regular.ttf', uni=True)
        pdf_file.add_font("Golos", "B", f'{self.util_files_dir}/golos-text_bold.ttf', uni=True)

    def __set_font_for_russian_language(self, pdf_file: FPDF, size: int):
        pdf_file.set_font("Golos", size=size)
