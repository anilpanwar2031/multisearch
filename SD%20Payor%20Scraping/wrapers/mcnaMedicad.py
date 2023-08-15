from mapPDF import mapEligibilityPatientVerification
from datetime import datetime
import json
from re import search

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

def merge_json_objects(*json_objects):
    combined_dict = {}
    for json_object in json_objects:
        dict_object = json.loads(json_object)
        combined_dict.update(dict_object)
    combined_json = json.dumps(combined_dict)
    return combined_json

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


def main(Scraperdata, request):
    patientdata = request.get("PatientData")[0]
    EligibilityPatient1 = Scraperdata.get("EligibilityPatientVerification")
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")
    EligibilityTreatmentHistory = Scraperdata.get("EligibilityServiceTreatmentHistory")
    EligibilityOtherProvisionsData = Scraperdata.get("EligibilityOtherProvisions")
    TreatmentHistorySummaryData = Scraperdata.get("TreatmentHistorySummary")
    EligibilityDeductiblesProcCodeData = Scraperdata.get("EligibilityDeductiblesProcCode")
    EligibilityFiles = Scraperdata.get("EligibilityFiles")

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]

    EligibilityPatient = ""
    for item in EligibilityPatient1:
        if item.get("subcriberID", None):
            EligibilityPatient  = item
        if item.get("PlanName",None):
            if item.get("TerminationDate") == "":
                EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
                EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":item.get("EffectiveDate")})
                EligibilityPatientVerification.update({"FamilyMemberEndDate":item.get("TerminationDate")})
    
           
    if ("Subscriber is Eligible" in EligibilityPatient.get("egibilityText")):
        EligibilityPatientVerification.update({"EligibilityStatus":"Active"})

    

    EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":EligibilityPatient.get("dateofbirth").replace("Date of Birth:\n","")}) 
    EligibilityPatientVerification.update({"FamilyMemberId":EligibilityPatient.get("subcriberID").replace("Subscriber ID:\n","")})
    EligibilityPatientVerification.update({"FamilyMemberName":EligibilityPatient.get("patientName")})
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName")})
    EligibilityPatientVerification.update({"PlanType":EligibilityPatient.get("Plan").replace("Plan:\n","")})
    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":EligibilityPatient.get("Plan").replace("Plan:\n","")})
    EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("group").replace("Group:\n","")})

    
    #EligibilityPatientVerification.update({"InNetworkOutNetwork":"In Network"})
    #EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    #EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":EligibilityPatient.get("DependentAge")})
    #EligibilityPatientVerification.update({"DependentStudentAgeLimit":EligibilityPatient.get("studentAge")})
    # #EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":EligibilityPatient.get("WaitingPeriod")})
    #EligibilityPatientVerification.update({"OrthodonticAgeLimits":EligibilityPatient.get("OrthoAge")})
    # # EligibilityPatientVerification.update({"MissingToothClause":EligibilityPatient.get("MissingToothClause")})
    # # EligibilityPatientVerification.update({"CoordinationofBenefitsType":EligibilityPatient.get("CoordinaitonOfBenefit")})

    

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

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Medicad payors\mcna\SD%20Payor%20Scraping\mcna.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Medicad payors\mcna\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data, request)
# with open("mcnaMedicad-patient.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
