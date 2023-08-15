from Utilities.pdf_utils import *
from FileDownload import Downloader
from mapPDF import mapEligibilityPatientVerification
from typing import Iterable
import re
from collections import defaultdict

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



def main(Scraperdata, request):

    patientdata = request.get("PatientData")[0]
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityDEductible = Scraperdata.get("EligibilityDeductible")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")
    EligibilityTreatmentHistory = Scraperdata.get("EligibilityServiceTreatmentHistory")
    EligibilityOtherProvisions = Scraperdata.get("EligibilityOtherProvisions")
    EligibilityFiles = Scraperdata.get("EligibilityFiles")
  


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
        "SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName"),
        "FamilyMemberName":patientdata.get("LastName")+", "+patientdata.get("FirstName").upper(),
        "FamilyMemberDateOfBirth":patientdata.get("BirthDate"),
        "Relationship":EligibilityPatient[0].get("Relationship"),
        "SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate"),
        "FamilyMemberEffectiveDate":EligibilityPatient[0].get("ProviderEffectiveDate"),
        "FamilyMemberEndDate":EligibilityPatient[0].get("ProviderTerminationDate"),
        "GroupName":EligibilityPatient[0].get("Plan"),
        # "ClaimsAddress":EligibilityPatient[0].get("PrimaryAddress"),
        "Gender":EligibilityPatient[0].get("Gender"),
        "EligibilityStatus":"Active"
        }
    )
    

     

    EligibilityMaximums.append({
                "Type":  "Lifetime Maximum",
                "Network": "In Network",
                "Amount": "",
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })
    EligibilityMaximums.append({
                "Type":  "Annual Maximum",
                "Network": "In Network",
                "Amount": "",
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })     
    EligibilityMaximums.append({
                "Type":  "Orthodontic Lifetime",
                "Network": "In Network",
                "Amount": "",
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })  
       


    EligibilityDeductiblesProcCode.append({
                "Type":  "Annual Deductible",
                "Network": "In Network",
                "Amount": "",
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            }) 
    EligibilityDeductiblesProcCode.append({
                "Type":  "Annual Deductible",
                "Network": "In Network",
                "Amount": "",
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Family"
            }) 



    output={}

    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityFiles":EligibilityFiles})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})    
    return output


