
import random,string
from FileDownload import Downloader
import tika
from tika import parser

def filedownload_(url):

    file_path = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + ".pdf"
    print(file_path)
    input_file = url.replace("%20", " ")
    print("input_file>>>>>>>>>>>>>>", input_file)
    Downloader('Revenue Cycle Management', file_path, input_file)
    return file_path

def pdf_scraper(inputfile):
    tika.initVM()
    parsed_pdf = parser.from_file(inputfile)
    pdf_content = parsed_pdf['content']

    temp={
        'GroupPolicyNumber':pdf_content.split('GROUP POLICY NUMBER')[1].split('\n\n')[0].strip(),
          'BenefitPeriod':pdf_content.split('BENEFIT PERIOD')[1].split('\n\n')[0].strip(),
          'CoverageType':pdf_content.split('COVERAGE TYPE')[1].split('\n\n')[0].strip(),
          'CoverageEffectiveDate':pdf_content.split('Coverage effective date:')[1].split('\n')[0].strip(),
          'CoverageTermDate':pdf_content.split('Coverage term date:')[1].split('\n')[0].strip(),
          'DependentAgeLimit':pdf_content.split('DEPENDENT AGE LIMIT')[1].split('\n\n')[0].strip(),
          'PatientEffectiveDate':pdf_content.split('Patient Effective Date:')[1].split('\n')[0].strip(),
          'EligibilityStatus':pdf_content.split('Patient Effective Date:')[1].split('\n\n')[1].split(' ')[-1],
          'FullTimeStudentAgeLimit':pdf_content.split('FULL TIME STUDENT AGE LIMIT')[1].split('\n\n')[0].strip(),
          'Dependency':' '.join(pdf_content.split('Patient Effective Date:')[1].split('\n\n')[1].split(' ')[:-1])
          }
    return temp

def main(data):
    """
        This function takes in a dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.
        It modifies keys of the RcmEobClaimDetail.

        Args:
        - data: A dictionary containing two lists: 'RcmEobClaimMaster' and 'RcmEobClaimDetail'.

        Returns:
        - A modified 'data' dictionary with the changed keys in 'RcmEobClaimDetail'.
    """
    for i in range(len(data['RcmEobClaimMaster'])):
        url = data["RcmEobClaimMaster"][i]["url"].replace('%20', ' ')
        pdf_file=filedownload_(url)
        temp_data=pdf_scraper(pdf_file)
        data['RcmEobClaimMaster'][i].update(temp_data)

    for i in range(len(data['RcmEobClaimMaster'])):
        cl_no=data['RcmEobClaimMaster'][i]['ClaimNumber'].split(' ')[1]
        patient=data['RcmEobClaimMaster'][i]['ClaimNumber'].split('for')[-1].strip()
        data['RcmEobClaimMaster'][i]['ClaimNumber']=cl_no
        data['RcmEobClaimMaster'][i]['Patient']=patient
    # Keys to modify in claim detail list
    keys=["Proccode","Status","DOS","ToothSurface","ToothNumbers","SubmittedAmount","PaidAmount"]
    temp=[]
    for i in range(len(data['RcmEobClaimDetail'])):
        final_dict = dict(zip(keys, list(data['RcmEobClaimDetail'][i].values())))
        temp.append(final_dict)
    data['RcmEobClaimDetail']=temp

    

    return data






