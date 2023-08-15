from mapPDF import mapEligibilityPatientVerification
from datetime import datetime
import json
from re import search

#PDF WRapper 
import json
import sys
from collections import ChainMap
from mapPDF import mapEligibilityPatientVerification
from datetime import datetime
import json
from re import search
from pdfFormator import Processor
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from FileDownload import Downloader
import random,string
# from utilities.pdf_utils import extract_pdf_and_zip, zip_processor, json_getter, get_address_string, extract_address_details
from pprint import pprint
import tabula



def changeNone(text):
    if(text=="None" or text=="N/A" or text==None):
        return ""
    else:
        return text
def calculate_difference(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    difference=f'${float(a)-float(b)}'
    if(difference=="$0.00"): return "0.00"
    return f'${round(float(a)-float(b) , 2)}'
def getsum(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    return f'${float(a)+float(b)}'

def get_substring_between_strings(s, start, end):
    """
    Function to get a substring between two strings.
    Args:
        s (str): Input string
        start (str): Starting string
        end (str): Ending string

    Returns:
        str: Substring between start and end strings, or None if not found.
    """
    start_index = s.find(start)
    if start_index == -1:
        return None

    end_index = s.find(end, start_index + len(start))
    if end_index == -1:
        return None

    substring = s[start_index + len(start):end_index]
    return substring

# def main(data):

def ScrapePDF(data):

    file_path =''.join(random.choices(string.ascii_uppercase +string.digits, k=10)) + ".pdf"
    print(file_path)
    input_file = data["EligibilityPatientVerification"][0]["url"][0].replace("%20", " ")
    #print("input_file>>>>>>>>>>>>>>",input_file)
    Downloader('Eligibility',file_path,input_file)

    df = tabula.read_pdf(file_path, 
                     guess=False, pages='1', stream=True , encoding="utf-8", 
                     area = (245.95837045669555,23.715, 726.3783704566956,582.165))
   
    
    df=df[0]
    df =df.set_axis(["key","value"], axis=1, copy=False)
    json_data =dict(zip(df['key'], df['value']))

    df_address = tabula.read_pdf(file_path, 
                     guess=False, pages='1', stream=True , encoding="utf-8", 
                     area = (70.7625,29.681990661621093, 158.7375,243.1169906616211))
    
    addr = ' '.join(df_address[0]['Delta Dental of Colorado'].to_list())
    addr = f'Delta Dental of Colorado {addr}'
    add = df_address[0]['Delta Dental of Colorado'].to_list()
    json_data['electronic_payer_id'] = add.pop(-1).split(':')[-1].strip()
    json_data['address'] = f"Delta Dental of Colorado {' '.join(add[:-1])}"  

    # print(json_data['electronic_payer_id'])    
    
    new_dict ={}
    data["EligibilityPatientVerification"][0].update(
        {'SubscriberId': str(json_data['Subscriber ID:']).strip(),
         'Relationship': str(json_data['Relationship:']).strip(),
         'PatientDOB': str(json_data['Patient DOB:']).strip(),
         'CoordinationofBenefits': str(json_data['Coordination of Benefits:']).strip(),
         'AlternateBenefits': str(json_data['Alternate Benefits:']).strip(),
         'DependentAgeLimit': str(json_data['Dependent Age Limit:']).strip(),
         'StudentAgeLimit': str(json_data['Student Age Limit:']).strip(),
         'electronicpayer_id': str(json_data['electronic_payer_id']).strip(),
         'OrthodonticAgeMinMax': str(json_data['Orthodontic Age Min/Max:']).strip(),
         'Claimaddress': str(json_data['address']).strip()
        }
        )  

    # print(data["EligibilityPatientVerification"])    

    return data




def main(Scraperdata, request):

    pdf_data = ScrapePDF(Scraperdata)
    # print(pdf_data)

    patientdata = request.get("PatientData")[0]
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")
    EligibilityTreatmentHistory = Scraperdata.get("EligibilityServiceTreatmentHistory")
    EligibilityOtherProvisions = Scraperdata.get("EligibilityOtherProvisions")

    #print(EligibilityPatient)

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]



    EligibilityPatientVerification.update(
        {
        "FamilyMemberId":patientdata.get("SubscriberId", ''),
        "SubscriberId":patientdata.get("SubscriberId"),
        "SubscriberName":patientdata.get("SubscriberName"),
        "InsuranceIDnumber":EligibilityPatient[0].get("InsuranceIDnumber"),
        "FamilyMemberName":EligibilityPatient[0].get("Name"),
        "FamilyMemberDateOfBirth":patientdata.get("BirthDate"),
        "Relationship":EligibilityPatient[0].get("Relationship"),
        "SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate"),
        "FamilyMemberEffectiveDate":EligibilityPatient[0].get("Effectivedate"),
        "FamilyMemberEndDate":EligibilityPatient[0].get("Terminationdate"),
        "InsuranceFeeScheduleUsed":EligibilityPatient[0].get("Product"),
        "GroupName":EligibilityPatient[0].get("Groupname"),
        "GroupNumber":EligibilityPatient[0].get("Groupnumber"),
        "DependentStudentAgeLimit":EligibilityPatient[0].get("StudentAgeLimit"),
        "DependentChildCoveredAgeLimit":EligibilityPatient[0].get("DependentAgeLimit"),
        "InsuranceCalendarOrFiscalPolicyYear":EligibilityPatient[0].get("CalendarorFiscalPolicyYear"),
        "InNetworkOutNetwork":"In Network",
        "oonBenefits":"Yes",
        "CoordinationofBenefitsType":EligibilityPatient[0].get("CoordinationofBenefits"),
        "CoordinationofBenefits":"Yes",
        "AlternativeBenefitProvision":EligibilityPatient[0].get("AlternateBenefits"),
        "MissingToothClause":"No",
        "EligibilityStatus":"Active",
        "ClaimsAddress":EligibilityPatient[0].get("Claimaddress"),
        "ClaimMailingAddress":EligibilityPatient[0].get("Claimaddress"),
        "OrthodonticAgeLimits":EligibilityPatient[0].get("OrthodonticAgeMinMax"),
        "ClaimPayerID":EligibilityPatient[0].get("electronicpayer_id")
        }
    )

    


    
    try:
        EligibilityPatientVerification.update({"IndividualAnnualDeductible":EligibilityPatient[0].get("IndividualAnnualDeductiblePPO").replace("Total allowed: ","")})
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":EligibilityPatient[0].get("IndividualAnnualDeductibleMetPPO").split("/")[0].replace("Used:","").strip()})
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":EligibilityPatient[0].get("IndividualAnnualDeductibleMetPPO").split("/")[1].replace("Remaining:","").strip()})
    except:
        pass
    
    
    try:
        EligibilityPatientVerification.update({"FamilyAnnualDeductible":EligibilityPatient[0].get("CalanderFamilyDeductiblePPO").replace("Total allowed: ","")})
        EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":EligibilityPatient[0].get("CalanderFamilyDeductibleMetPPO").split("/")[0].replace("Used:","").strip()})
        EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":EligibilityPatient[0].get("CalanderFamilyDeductibleMetPPO").split("/")[1].replace("Remaining:","").strip()})
    except:
        pass


    try:
        EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":EligibilityPatient[0].get("LifetimeMaximumBenefitsPPO").replace("Total allowed: ","")})
        EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":EligibilityPatient[0].get("BenefitsUsedtoDatePPO").split("/")[0].replace("Used:","").strip()})
        EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":EligibilityPatient[0].get("BenefitsUsedtoDatePPO").split("/")[1].replace("Remaining:","").strip()})
    except:
        pass


    try:
        EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":EligibilityPatient[0].get("AnnualMaximumBenefitsPPO").replace("Total allowed: ","")})
        EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":EligibilityPatient[0].get("AnnualMaximumBenefitsUsedtoDate").split("/")[0].replace("Used:","").strip()})
        EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":EligibilityPatient[0].get("AnnualMaximumBenefitsUsedtoDate").split("/")[1].replace("Remaining:","").strip()})
    except:
        pass


    try:
        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":EligibilityPatient[0].get("OrthodonticLifetimeBenefit").replace("Total allowed: ","")})
        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":EligibilityPatient[0].get("OrthodonticAgeLimit").split("/")[0].replace("Used:","").strip()})
        EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":EligibilityPatient[0].get("OrthodonticAgeLimit").split("/")[1].replace("Remaining:","").strip()})
    except:
        pass





    ####----Maximums and deductibles-----###
    
    EligibilityMaximums.append({
                "Type":  "Lifetime Maximum",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits"),
                "Remaining": EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit"),
                "Used": EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })
    EligibilityMaximums.append({
                "Type":  "Annual Maximum",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits"),
                "Remaining": EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit"),
                "Used": EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })     
    EligibilityMaximums.append({
                "Type":  "Orthodontic Lifetime",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("OrthodonticLifetimeBenefit"),
                "Remaining": EligibilityPatientVerification.get("OrthodonticLifetimeRemainingBenefit"),
                "Used": EligibilityPatientVerification.get("OrthodonticLifetimeBenefitUsedtoDate"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })  
    # try:
    #     EligibilityMaximums.append({
    #                 "Type":  "Dental Benefit",
    #                 "Network": "In Network",
    #                 "Amount": EligibilityPatient[0].get("DentalBenefitUsedtoDate").replace("Total allowed: ",""),
    #                 "Remaining": EligibilityPatient[0].get("DentalBenefitUsedtoDate").split("/")[0].replace("Used:","").strip(),
    #                 "Used": EligibilityPatient[0].get("DentalBenefitUsedtoDate").split("/")[1].replace("Remaining:","").strip(),
    #                 "ServiceCategory": "Dental",
    #                 "BenefitPeriod": "",
    #                 "Family_Individual": "Individual"
    #             })
    # except:
    #     pass

    


    EligibilityDeductiblesProcCode.append({
                "Type":  "Annual Deductible",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("IndividualAnnualDeductible"),
                "Remaining": EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining"),
                "Used": EligibilityPatientVerification.get("IndividualAnnualDeductibleMet"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            }) 
    EligibilityDeductiblesProcCode.append({
                "Type":  "Annual Deductible",
                "Network": "In Network",
                "Amount": EligibilityPatientVerification.get("FamilyAnnualDeductible"),
                "Remaining": EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining"),
                "Used": EligibilityPatientVerification.get("FamilyAnnualDeductibleMet"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Family"
            }) 

  
    
    for item in EligibilityBenefitsData:
        limitation = ""
        Agelimit = ""
        history = ""
        flag = 0
        for hist in EligibilityMaximiums:
            typebenefit = hist.get("Type").split(" ")[0]
            if search(typebenefit, item.get("Benefitclass")):
                flag = 1
                limitation = hist.get("HowManyAllowed?")
                Agelimit = hist.get("AgeLimit")
                history = hist.get("NextAvailable")
            elif search(typebenefit.upper(), item.get("Procedurecode")):
                flag = 1
                limitation = hist.get("HowManyAllowed?")
                Agelimit = hist.get("AgeLimit")
                history = hist.get("NextAvailable")

        EligibilityBenefits.append({
            "ProcedureCode": item.get("Proccode"),
            "ProcedureCodeDescription": item.get("Procedurecode").replace(item.get("Proccode"),"").strip(" -"),
            "Amount": "",
            "Type": item.get("Benefitclass"),
            "limitation": str(limitation+" "+Agelimit).replace(" N/A",""),
            "DeductibleApplies": item.get("DeductibleWaived"),
            "Copay": item.get("Copay"),
            "WaitingPeriod": item.get("WaitingPeriod")
        })
        if flag == 1:
            TreatmentHistorySummary.append({
                "ProcedureCode": item.get("Proccode"),
                "LimitationText": str(limitation+" "+Agelimit).replace(" N/A",""),
                "History": history,
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": item.get("Procedurecode").replace(item.get("Proccode"),"").strip(" -")
            })
            EligibilityServiceTreatmentHistory.append({
                "ProcedureCode": item.get("Proccode"),
                "LimitationText": str(limitation+" "+Agelimit).replace(" N/A",""),
                "History": history,
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": item.get("Procedurecode").replace(item.get("Proccode"),"").strip(" -")
            })
        if item.get("Proccode") == "D2391":
            EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":item.get("WaitingPeriod")})



    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output





# if __name__ == "__main__":
#     request = json.load(open(r"C:\BPK\Eligibility_Python\VSCODE\26_06\SD Payor Scraping\DeltadentalColorado.json", 'r'))
#     json_data=json.load(open(r"C:\BPK\Eligibility_Python\VSCODE\26_06\SD Payor Scraping\64467_output.json", 'r'))
#     data = main(json_data,request)
#     with open("ColoradoOutput_64467_output", "w") as outfile:
#         json.dump(data, outfile, indent=4)



# request=json.load(open(r"C:\BPK\Eligibility_Python\VSCODE\12_04\SD Payor Scraping\DeltadentalColorado.json", 'r'))
# data=json.load(open(r"C:\BPK\Eligibility_Python\VSCODE\12_04\SD Payor Scraping\output.json", 'r'))
# output=main(data, request)
# with open("ColoradoOutput_Kali_Sabedra.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
