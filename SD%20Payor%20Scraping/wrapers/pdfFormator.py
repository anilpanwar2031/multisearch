from adobe.pdfservices.operation.auth.credentials import Credentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.execution_context import ExecutionContext
from adobe.pdfservices.operation.io.file_ref import FileRef
from adobe.pdfservices.operation.pdfops.extract_pdf_operation import ExtractPDFOperation
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_pdf_options import ExtractPDFOptions
from adobe.pdfservices.operation.pdfops.options.extractpdf.extract_element_type import ExtractElementType

import os.path
import zipfile
import json
import pandas as pd
import logging


class Processor:

    def __init__(self, input_file):
        self.input_file = input_file
        print("self.input_file>>>>>>>>>>>>>>>>",self.input_file)

    def zip_processor(self,):
        output_zip = "./ExtractTextInfoFromPDF12.zip"

        if os.path.isfile(output_zip):
            os.remove(output_zip)

        input_pdf = self.input_file


        try:

            # Initial setup, create credentials instance.
            credentials = Credentials.service_account_credentials_builder().from_file(
                "pdfservices-api-credentials.json").build()

            # Create an ExecutionContext using credentials and create a new operation instance.
            execution_context = ExecutionContext.create(credentials)
            extract_pdf_operation = ExtractPDFOperation.create_new()

            # Set operation input from a source file.
            source = FileRef.create_from_local_file(input_pdf)
            extract_pdf_operation.set_input(source)

            # Build ExtractPDF options and set them into the operation
            extract_pdf_options: ExtractPDFOptions = ExtractPDFOptions.builder() \
                .with_element_to_extract(ExtractElementType.TEXT) \
                .with_element_to_extract(ExtractElementType.TABLES) \
                .build()
            extract_pdf_operation.set_options(extract_pdf_options)

            # Execute the operation.
            result: FileRef = extract_pdf_operation.execute(execution_context)

            # Save the result to the specified location.
            result.save_as(output_zip)

            print("Successfully extracted information from PDF. Printing H1 Headers:\n")

            archive = zipfile.ZipFile(output_zip, 'r')
            jsonentry = archive.open('structuredData.json')
            jsondata = jsonentry.read()
            data = json.loads(jsondata)
            for element in data["elements"]:
                if (element["Path"].endswith("/H1")):
                    print(element["Text"])

        except (ServiceApiException, ServiceUsageException, SdkException):
            logging.exception("Exception encountered while executing operation")

        return output_zip


    def dfGetter(self, output_zip):

        archive = zipfile.ZipFile(output_zip, 'r')
        file_names = archive.namelist()
        table_files = [name for name in file_names if name.startswith('tables/') and name.endswith(".xlsx")]

        dict_list = []

        for idx, name in enumerate(table_files):
            with archive.open(name) as file:
                try:
                    df = pd.read_excel(file)
                    if df.apply(lambda x: x.astype(str).str.contains('_x000D_').any()).any():
                        df = df.replace('_x000D_', '', regex=True)
                    if any('_x000D_' in col for col in df.columns):
                        df = df.rename(columns=lambda x: x.replace("_x000D_", ""))
                    dict_list.append(df)
                except pd.errors.ParserError as e:
                    logging(f"Error parsing {name}: {e}")


        return dict_list

