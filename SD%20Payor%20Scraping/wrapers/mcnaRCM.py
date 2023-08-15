import pdfplumber
import fitz
from FileDownload import Downloader
import random, string


def filedownload_(url):
    file_path = (
            "".join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".pdf"
    )
    print(file_path)
    input_file = url.replace("%20", " ")

    Downloader("Revenue Cycle Management", file_path, input_file)

    return file_path
def get_plumber_texts(file_path):
    tt = ''
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        for page in pdf.pages:
            texts = page.extract_text()
            tt = tt + texts
    return tt


def get_flitz_texts(file_path):
    with fitz.open(file_path) as pdf:
        texts = ''
        for page_number in range(pdf.page_count):
            page = pdf.load_page(page_number)
            text = page.get_text()
            texts = texts + ' ' + text
    return texts


def clean_claiMmaster(claimmaster, texts):
    claimmaster.update({'PayeeAddress':claimmaster['FacilityAddress1']+' '+claimmaster['FacilityAddress2']})
    del claimmaster['FacilityAddress1']
    del claimmaster['FacilityAddress2']

    for line in texts.split('\n'):
        if 'Facility Name' in line:
            fn = line.split(': ')[1]
            claimmaster.update({'PayeeName': fn})
            del claimmaster['FacilityName']
        if 'Facility Phone' in line:
            phone = line.split(': ')[1]
            claimmaster.update({'PayeePhone': phone})

    return claimmaster


def get_claimMaster(data,texts):
    print("IN THE CLAIMMASTER")
    master = data['RcmEobClaimMaster'][0]
    firstname = master['FirstName'].split('\n')[1]
    lastname = master['LastName'].split('\n')[1]
    processed = master['Processed'].split('\n')[1]
    claimmaster = {
        'ClaimNumber': master['ClaimId'].split('#')[1].split(' ')[0],
        'SubmittedDate': master['SubmittedDate'].split('\n')[1],
        "DateOfBirth": master['DateOfBirth'].split('\n')[1],
        "SubscriberId": master['SubscriberId'].split('\n')[1],
        "FirstName": firstname,
        "LastName": lastname,
        "Zip": master['Zip'].split('\n')[1],
        "FacilityName": master['FacilityName'],
        "FacilityAddress1": master['FacilityAddress1'].split('\n')[1],
        "FacilityAddress2": master['FacilityAddress2'],
        "ProviderName": master['TreatingProvider'].split('\n')[1].split('(')[0].strip(),
        "ProviderLocation": master['TreatmentLocation'].split('\n')[1],
        "RenderingProvider": master['TreatingProvider'].split('\n')[1].split('(')[0].strip(),
        "EnteredBy": master['EnteredBy'].split('\n')[1],
        "url": master['url'],
        "RcmGridViewId": 0
    }
    patientname = firstname+' '+lastname
    claimmaster.update({'PatientName': patientname, 'ClaimStatus': master['Status'], 'DateProcessed': processed})
    claimmaster = clean_claiMmaster(claimmaster, texts)

    return claimmaster


def get_claimdetails(data, texts):
    details = data['RcmEobClaimDetail'][:-1]
    texts_list = texts.split('\n')
    k = 0
    l = 0
    for det in details:
        k = k + l
        texts_l = texts_list[k:]
        desc = det['Description'].split(' ')[0]
        tt = ''
        for i, t in enumerate(texts_l):
            tlist = texts_l[i].split(' ')
            if desc in tlist:
                tt = tt + texts_l[i]
                for j in range(i + 1, len(texts_l)):
                    if '$' in texts_l[j]:
                        l = j
                        break
                    else:
                        tt = tt + ' ' + texts_l[j]
                break
        det['Description'] = tt
    for d in details:
        ds = d['Description'].split(' ')[2:]

        d['Description'] = " ".join(ds)
        d['ProcedureDate'] = d['Proceduredate']
        d['ProcedureCode'] = d['Cdt']
        d['AreaOrTooth'] = d['AreaOrtooth#']
        d['BilledAmount'] = d['Billedamount']
        d['PaidAmount'] = d['Paidamount']
        d["RcmGridViewId"] = 0
        del d['Cdt']
        del d['AreaOrtooth#']
        del d['Proceduredate']
        del d['Billedamount']
        del d['Paidamount']
        if d['AreaOrTooth'] == d['Description'].split(' ')[-1]:
            d['Description'] = d['Description'][:-1].strip()

    return details


def main(data):
    print("\n")
    print("\n")
    print("\n")
    print("\n")

    url = data["RcmEobClaimMaster"][0]["url"]
    print("main 1")

    file_path = filedownload_(url.replace("%20", " "))
    texts = get_plumber_texts(file_path)
    flitz_texts = get_flitz_texts(file_path)

    claimMaster = get_claimMaster(data, texts)
    claimMaster = [claimMaster]
    claimdetails = get_claimdetails(data, flitz_texts)

    json_data = {
        'RcmEobClaimMaster': claimMaster,
        'RcmEobClaimDetail': claimdetails,
        'EligibilityFiles': data["EligibilityFiles"]
    }
    return json_data




