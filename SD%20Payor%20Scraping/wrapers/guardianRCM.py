import pdfplumber
import tika
tika.initVM()
from Utilities.pdf_utils import *
from FileDownload import Downloader

import tabula
import pandas as pd
from PyPDF2 import PdfReader

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import random, string


def filedownload_(url):
    """
    To download pdf from blob url
    Args:
        url:
    Returns:
        filepath of pdf
    """
    file_path = (
            "".join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".pdf"
    )
    print(file_path)
    input_file = url.replace("%20", " ")

    Downloader("Revenue Cycle Management", file_path, input_file)

    return file_path


def getAllTexts(file_path):
    texts = ' '
    with open(file_path, 'rb') as file:
        # Create a PdfReader object
        pdf = PdfReader(file)

        for page in pdf.pages:
            text = page.extract_text()
            texts = texts + text + ' '
    return texts


def remove_duplicate_dict(data_list):
    unique_dicts = list(set(map(lambda x: tuple(sorted(x.items())), data_list)))
    if len(unique_dicts) < len(data_list):
        return [dict(t) for t in unique_dicts]
    else:
        return data_list



def extract_text_coordinates(file_path):
    text_list = []
    with pdfplumber.open(file_path) as pdf:
        # Iterate through each page of the PDF
        for page_number in range(len(pdf.pages)):
            page = pdf.pages[page_number]
            page_number = page_number + 1
            # Extract the text content and its coordinates
            for element in page.extract_words(x_tolerance=1, y_tolerance=1, keep_blank_chars=True):
                text_dict = {}
                text = element["text"]
                x, y = element["x0"], element["top"]

                text_cord = f"Page {page_number + 1}: Text: {text} Coordinates: X={x}, Y={y}"
                text_dict.update({'page': page_number, 'text': text, 'cordx': x, 'cordy': y})
                text_list.append(text_dict)
    return text_list

def get_details(file_path, texts):

    text_list = extract_text_coordinates(file_path)
    pdf_path = file_path
    dfs = []
    x2 = 0
    y2 = 0
    for text_d in text_list:
        x = text_d['cordx']
        y = text_d['cordy']
        if x2 < x:
            x2 = text_d['cordx']
        if y2 < y:
            y2 = text_d['cordy']
    x2 = x2 + 20
    y2 = y2 + 20
    # print("YYYY", y2)
    for i in range(len(text_list)):
        x1 = y1 = ''
        if 'Line' in text_list[i]['text']:
            # print("Line", text_list[i]['text'])
            x1 = text_list[i]['cordx']
            y1 = text_list[i]['cordy']
            page_number = text_list[i]['page']
            for j in range(i, len(text_list)):

                if page_number == text_list[j]['page']:
                    if 'BENEFIT SUMMARY' in text_list[j]['text']:
                        # print("Bene", text_list[j]['text'])
                        # print("PAG", text_list[j]['page'])
                        page = int(text_list[j]['page'])
                        y2 = text_list[j]['cordy']
                        # print(f"x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}")
                        tabula_dfs = tabula.read_pdf(pdf_path, guess=False, pages=page, stream=True, encoding="utf-8",
                                                     area=(y1, x1, y2, x2), multiple_tables=True)
                        df_filled = tabula_dfs[0].fillna('')
                        dfs.append(df_filled[1:])
                        break

                if page_number == text_list[j]['page']:
                    if '10 Hudson Yards' in text_list[j]['text']:
                        # print("10 Hudson", text_list[j]['text'])
                        # print("PAG", text_list[j]['page'])
                        page = int(text_list[j]['page'])
                        y2 = text_list[j]['cordy']
                        # print(f"x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}")
                        tabula_dfs = tabula.read_pdf(pdf_path, guess=False, pages=page, stream=True, encoding="utf-8",
                                                     area=(y1, x1, y2, x2), multiple_tables=True)
                        df_filled = tabula_dfs[0].fillna('')
                        dfs.append(df_filled[1:])
                        break

                if page_number == text_list[j]['page']:
                    #                 if 'BENEFIT SUMMARY' not in text_list[j]['text'] and '10 Hudson Yards' not in text_list[j]['text']:
                    if 'VNE' in text_list[j]['text']:
                        y2 = 780
                        page = int(text_list[j]['page'])
                        # print(f"x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}")
                        tabula_dfs = tabula.read_pdf(pdf_path, guess=False, pages=page, stream=True, encoding="utf-8",
                                                     area=(y1, x1, y2, x2), multiple_tables=True)
                        df_filled = tabula_dfs[0].fillna('')
                        dfs.append(df_filled[1:])
                        break

        search_string = 'TOTALS'
        final = []
        stack_list = []
        for d in dfs:
            last_row = d.iloc[-1]
            col = last_row[4]

            # print(col)
            # print(type(col))
            if 'TOTALS' in col:
                print("In the if")
                if stack_list:
                    new_df = pd.concat(stack_list + [d], axis=0)
                    final.append(new_df)
                    stack_list = []
                else:
                    final.append(d)
            else:
                stack_list.append(d)


        tdfs = []

        for df in final:
            df = df[~df.apply(lambda row: row.astype(str).str.contains('TOTALS', case=False)).any(axis=1)]
            df.rename(columns={'Date of': 'Date'}, inplace=True)
            df.fillna('', inplace=True)
            df.drop('Line', axis=1, inplace=True)
            tdfs.append(df)

        new_dict = []
        for i, td in enumerate(tdfs):
            tab = td.to_dict(orient='records')
            for i in range(len(tab)):
                new_dict.append(tab[i])

        tab_dict = []

        change_keys = [("Alt", "AltCode"), ("Tooth", "ToothNo"), ("Date", "DateOfService"),
                       ("Submitted.1", "SubmittedCharge"),
                       ("Benefit", "BenefitAmount"), ("Considered", "ConsideredCharge"),
                       ("Deductible", "DeductibleAmount"), ("Covered", "CoveredCharge"),
                       ("Coverage", "CoveragePercent")]
        for d in new_dict:
            for k in change_keys:
                old_key = k[0]
                new_key = k[1]
                value = d[old_key]
                d[new_key] = value

            proccode = d['Submitted'].split('/')[0]
            description = d['Submitted'].split('/')[-1]

            d.update({'AltCode': proccode, 'Description': description})

            for k in change_keys:
                del d[k[0]]
            del d['Submitted']
            # print("D", d)
            tab_dict.append(d)

    return tab_dict



def main(data):
    url = data["RcmEobClaimMaster"][0]["url"]
    print("URLLLLLLLLLLLLLLLLLLLL", url)

    print("main 1")

    file_path = filedownload_(url.replace("%20", " "))

    texts = getAllTexts(file_path)
    eobclaimdetail = get_details(file_path, texts)


    json_data = {
        'RcmEobClaimMaster': data['RcmEobClaimMaster'],
        'RcmEobClaimDetail': eobclaimdetail
    }

    for i, (claim1,claim2) in enumerate(zip(
            json_data["RcmEobClaimMaster"],
            json_data["RcmEobClaimDetail"]
    ),
            start=1, ):
        claim1["RecordId"] = i
        claim2["RecordId"] = i


    return json_data


