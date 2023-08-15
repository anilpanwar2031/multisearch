import sys
import os
import uuid
import tabula

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
import json
from FileDownload import Downloader
import random, string
from PyPDF2 import PdfReader
import re
from Utilities.pdf_utils import *


def replace_strip(t):
    return t.replace('\n', '').strip()


def find_item(text, start_string, end_string):
    item = ''
    if start_string in text:
        item = text.split(start_string, 1)[-1]
        if end_string in item:
            item = item.split(end_string, 1)[0]
        elif '\n' in item or '\r' in item:
            item = item.splitlines()[0]
    return item


def get_patientprovider(file_path):
    tabula_dfs = tabula.read_pdf(file_path, guess=False, pages=1, stream=True, encoding="utf-8",
                                 area=[(57, 3, 139, 168), (56, 194, 142, 378)],
                                 multiple_tables=True)

    add_col = tabula_dfs[0].columns[0]
    patientinfo = ' '.join(tabula_dfs[0][add_col].to_list())
    patient_address = extract_address_details(patientinfo)
    print("patient_address_details", patient_address)
    patient = {
        'PatientName': patient_address.get('ItemName', ''),
        'Address': patient_address.get('Item', ''),

    }
    # ####### Provider Information ################################
    add_col = tabula_dfs[1].columns[0]

    providerInfo = ' '.join(tabula_dfs[1][add_col].to_list())
    providerinfo = replace_strip(providerInfo.split(')')[2])
    providerid = replace_strip(providerInfo.split('(')[1].split(')')[0])
    providerclinicid = replace_strip(providerInfo.split('(')[2].split(')')[0])
    providerName = replace_strip(providerInfo.split('(')[0])
    providerClinicName = replace_strip(providerInfo.split(')')[1].split('(')[0])
    provider_address = extract_address_details(providerinfo)
    provider_address['ItemName'] = provider_address['ItemName'].split('Payee Name:')[1].strip()
    provider_address['AddressElements'] = provider_address['Item'].split('Payee Name:')[0].strip()
    provider = {
        'ProviderId': providerid,
        'ProviderName': providerName,
        'ProviderClinicName': providerClinicName,
        'ProviderClinicId': providerclinicid,
        'ProviderAddress': provider_address['AddressElements'],

    }
    patientprovider = {**patient, **provider}
    print("PATIENT PROVIDER", patientprovider)
    return patientprovider


def claiminformation(texts):
    if 'Missing Teeth' in texts:
        claiminfo = find_item(texts, 'Claim Information', 'Missing Teeth')
    else:
        claiminfo = find_item(texts, 'Claim Information', 'Service(s) Detail')

    claiminfo = {
        'ClaimCompany': replace_strip(claiminfo.split('Benefit Level:')[0]),
        'BenefitLevel': replace_strip(find_item(texts, 'Benefit Level:', 'Client Claim ID:')),
        'ClientClaimID': replace_strip(find_item(texts, 'Client Claim ID:', 'Date Received:')),
        'DateReceived': replace_strip(find_item(texts, 'Date Received:', 'Date Entered:')),
        'DateEntered': replace_strip(find_item(texts, 'Date Entered:', 'Date Paid:')),
        'EncounterID': replace_strip(find_item(texts, 'Encounter', 'Service(s) Detail')),
        'ClaimStatus': replace_strip(find_item(texts, 'Claim Status:', 'Missing Teeth')),
        'MissingTeeth': replace_strip(find_item(texts, 'Missing Teeth', 'Rendered:'))
    }

    return claiminfo


def paymentinformation(texts):
    paymentinfo = {
        'CheckNumber': replace_strip(find_item(texts, 'Check Number', 'Pay Member')),
        'PayMember': replace_strip(find_item(texts, 'Pay Member', 'Check Amount')),
        'CheckAmount': replace_strip(find_item(texts, 'Check Amount', 'Total Billed Amount')),
        'TotalBilledAmount': replace_strip(find_item(texts, 'Total Billed Amount', 'Check Status')),
        'CheckStatus': replace_strip(find_item(texts, 'Check Status', 'Original Paid Amount')),
        'OriginalPaidAmount': replace_strip(find_item(texts, 'Original Paid Amount', 'Check Date')),
        'CheckDate': replace_strip(find_item(texts, 'Check Date', 'Net Paid Amount')),
        'NetPaidAmount': replace_strip(find_item(texts, 'Net Paid Amount', 'Check Cleared')),
        'CheckCleared': replace_strip(find_item(texts, 'Check Cleared', 'EFT Flag / Acct')),
        'EftFlag': replace_strip(find_item(texts, 'EFT Flag / Acct', 'Rendered'))
    }

    return paymentinfo


def get_claimmaster(file_path, texts):
    patientprovider = get_patientprovider(file_path)
    claimInformation = claiminformation(texts)
    paymentInformation = paymentinformation(texts)
    return {**paymentInformation, **patientprovider, **claimInformation}


def get_claimdetail(file_path, texts):
    tabs = []
    pattern = r"D\d{4}\ -"
    tables = texts.split('Service(s) Detail')[1].split('Payment Information')[0]
    codes = re.findall(pattern, tables)
    # print("Codes", len(codes))
    # print("MATCH", codes)
    next = ''
    for i, c in enumerate(codes):
        if i == len(codes) - 1:
            t = next.split(codes[i], 1)[1]
            t = codes[i] + '' + t
            print("\n")
            print("LT", t)
            tabs.append(t)
        else:
            if next == '':
                next = tables.split(codes[i], 1)[1]
                t = tables.split(codes[i], 1)[1].split(codes[i + 1])[0]
                t = codes[i] + '' + t

                tabs.append(t)
            else:
                next = next.split(codes[i], 1)[1]

                t = next.split(codes[i + 1], 1)[0]
                t = codes[i] + '' + t
                tabs.append(t)

    tab_list = []
    for tab in tabs:
        proccode = tab.split('\n')[0]
        quantity = tab.split('Quantity')[1].split('\n')[1]
        deductible = tab.split('Deductible')[1].split('\n')[1]
        coinsuranceComputed = tab.split('Coinsurance Computed')[1].split('\n')[1]
        billedAmount = tab.split('Billed Amount')[1].split('\n')[1]
        serviceDate = tab.split('Service Date')[1].split('\n')[1]
        COBCollected = tab.split('COB Collected')[1].split('\n')[1]
        payable = tab.split('Payable')[1].split('\n')[1]
        allowedAmount = tab.split('Allowed Amount')[1].split('\n')[1]

        authNumber = tab.split('Auth Number')[1].split('\n')[1]
        if authNumber == 'Copay Computed':
            authNumber = ''

        copayComputed = tab.split('Copay Computed')[1].split('\n')[1]
        overMaximum = tab.split('Over Maximum')[1].split('\n')[1]
        paidAmount = tab.split('Paid Amount')[1].split('\n')[1]
        serviceLineDenial = ''
        if 'following reasons:' in tab:
            serviceLineDenial = tab.split('following reasons:\n')[1].replace("\n", '')

        tab_list.append({'ServiceCode': proccode, 'Quantity': quantity, 'Deductible': deductible,
                         'CoinsuranceComputed': coinsuranceComputed,
                         'BilledAmount': billedAmount, 'ServiceDate': serviceDate, 'COBCollected': COBCollected,
                         'Payable': payable,
                         'AllowedAmount': allowedAmount, 'AuthNumber': authNumber, 'CopayComputed': copayComputed,
                         'OverMaximum': overMaximum,
                         'PaidAmount': paidAmount, 'ServiceLineDenialException': serviceLineDenial})

    return tab_list


def main(data):
    dob = data['RcmEobClaimMaster'][0].get('DOB', '')
    url = data['RcmEobClaimMaster'][0].get('url', '')
    dos = data['RcmEobClaimMaster'][0].get('DateOfService', '')
    providername = data['RcmEobClaimMaster'][0].get('ProviderName', '')
    datepaid = data['RcmEobClaimMaster'][0].get('DatePaid', '')
    print()

    file_path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".pdf"
    print(file_path)
    input_file = data["RcmEobClaimMaster"][0]["url"].replace("%20", " ")
    print("input_file>>>>>>>>>>>>>>", input_file)
    Downloader('Revenue Cycle Management', file_path, input_file)

    texts = ''
    with open(file_path, 'rb') as file:
        pdf = PdfReader(file)
        for page in pdf.pages:
            text = page.extract_text()
            texts = texts + ' ' + text

    # Extract patient information
    claimmaster = []
    clmaster = get_claimmaster(file_path, texts)
    claimmaster.append(clmaster)
    claimdetail = get_claimdetail(file_path, texts)


    claimmaster[0].update(
        {'DOB': dob, 'url': url, 'DateOfService': dos, 'ProviderName': providername, 'DatePaid': datepaid})

    data = {
        'RcmEobClaimMaster': claimmaster,
        'RcmEobClaimDetail': claimdetail
    }

    return data
