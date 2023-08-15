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
    EligibilityOtherProvisions = Scraperdata.get("EligibilityOtherProvisions")
    TreatmentHistorySummaryData = Scraperdata.get("TreatmentHistorySummary")

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]

    EligibilityPatient = ""
    for item in EligibilityPatient1:
        if item.get("MemberName", None):
            EligibilityPatient  = item
        if item.get("Dob",None):
            if item.get("Dob") == patientdata.get("BirthDate"):
                if item.get("Status") == "Active":
                    EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
                EligibilityPatientVerification.update({"Relationship":item.get("Relationship")})
                EligibilityPatientVerification.update({"GroupNumber":item.get("ViewBenefitsgroup/Subgroup")})
                EligibilityPatientVerification.update({"FamilyMemberName":item.get("PatientName")})
        if item.get("Relationship") == "Subscriber":
            EligibilityPatientVerification.update({"SubscriberName":item.get("PatientName")})
            EligibilityPatientVerification.update({"SubscriberDateOfBirth":item.get("Dob")})
    


    EligibilityPatientVerification.update({"FamilyMemberId":patientdata.get("PatientMemberId")})
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"PlanType":EligibilityPatient.get("Program")})
    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":EligibilityPatient.get("Program")})
    EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":patientdata.get("BirthDate")})
    EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":EligibilityPatient.get("EffectiveDate")})
    EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":EligibilityPatient.get("MaximumDeductibleCalculated")})
    EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("GroupName")})
    EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":EligibilityPatient.get("WaitingPeriod")})
    EligibilityPatientVerification.update({"AlternativeBenefitProvision":EligibilityPatient.get("AlternativeBenefit").replace("Amalgam and Composite restorations are allowed with no frequency limitations.","").strip()})
    EligibilityPatientVerification.update({"MissingToothClause":EligibilityPatient.get("MissingToothClause")})
    EligibilityPatientVerification.update({"InNetworkOutNetwork":"In Network"})
    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})
    EligibilityPatientVerification.update({"OrthodonticAgeLimits":EligibilityPatient.get("Orthodontics")})
    EligibilityPatientVerification.update({"CoordinationofBenefitsType":EligibilityPatient.get("CoordinaitonOfBenefit")})
    EligibilityPatientVerification.update({"ClaimPayerID":"22229"})

    EligibilityPatientVerification.update({"ClaimMailingAddress":EligibilityOtherProvisions[0].get("ClaimMailingAddress").replace("\n"," ")})
    EligibilityPatientVerification.update({"ClaimsAddress":EligibilityOtherProvisions[0].get("ClaimMailingAddress").replace("\n"," ")})

    

    # ####----Maximums and deductibles-----###
    for itemMax in EligibilityMaximiums:
        if itemMax.get("type") == "Individual Deductible":
            EligibilityPatientVerification.update({"IndividualAnnualDeductible":itemMax.get("IndividualsAmount")})
            EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":itemMax.get("IndividualsUsed")})
            EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleMet").strip())})

            EligibilityDeductiblesProcCode.append({
                "Type": "Deductible",
                "Network": "In Network",
                "Amount": itemMax.get("IndividualsAmount"),
                "Remaining": EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining"),
                "Used": itemMax.get("IndividualsUsed"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })

            EligibilityPatientVerification.update({"FamilyAnnualDeductible":itemMax.get("FamilyAmount")})
            EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":itemMax.get("FamilyUsed")})
            EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualDeductible").strip(),EligibilityPatientVerification.get("FamilyAnnualDeductibleMet").strip())})

            EligibilityDeductiblesProcCode.append({
                "Type": "Deductible",
                "Network": "In Network",
                "Amount": itemMax.get("FamilyAmount"),
                "Remaining": EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining"),
                "Used": itemMax.get("FamilyUsed"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Family"
            })

        if itemMax.get("type") == "Individual Maximum":
            EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":itemMax.get("IndividualsAmount")})
            EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":itemMax.get("IndividualsUsed")})
            EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate").strip())})

            EligibilityMaximums.append({
                "Type": "Maximum",
                "Network": "In Network",
                "Amount": itemMax.get("IndividualsAmount"),
                "Remaining": EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit"),
                "Used": itemMax.get("IndividualsUsed"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })

            EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":itemMax.get("FamilyAmount")})
            EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":itemMax.get("FamilyUsed")})
            EligibilityPatientVerification.update({"FamilyAnnualRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("FamilyAnnualBenefitsUsedtoDate").strip())})
            EligibilityMaximums.append({
                "Type": "Maximum",
                "Network": "In Network",
                "Amount": itemMax.get("FamilyAmount"),
                "Remaining": EligibilityPatientVerification.get("FamilyAnnualRemainingBenefit"),
                "Used": itemMax.get("FamilyUsed"),
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Family"
            })


        if itemMax.get("type") == "Individual Lifetime Orthodontic Maximum":
            EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":itemMax.get("IndividualsAmount")})
            EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":itemMax.get("IndividualsUsed")})
            EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate").strip())})
            EligibilityMaximums.append({
                "Type": "Lifetime Maximum",
                "Network": "In Network",
                "Amount": itemMax.get("IndividualsAmount"),
                "Remaining": EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit"),
                "Used": itemMax.get("IndividualsUsed"),
                "ServiceCategory": "Orthodontic",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })


            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":itemMax.get("IndividualsAmount")})
            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":itemMax.get("IndividualsUsed")})
            EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("OrthodonticLifetimeBenefit").strip(),EligibilityPatientVerification.get("OrthodonticLifetimeBenefitUsedtoDate").strip())})

            EligibilityPatientVerification.update({"FamilyLifetimeMaximumBenefits":itemMax.get("FamilyAmount")})
            EligibilityPatientVerification.update({"FamilyLifetimeBenefitsUsedtoDate":itemMax.get("FamilyUsed")})
            EligibilityPatientVerification.update({"FamilyLifetimeRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("FamilyLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("FamilyLifetimeBenefitsUsedtoDate").strip())})
            EligibilityMaximums.append({
                "Type": "Lifetime Maximum",
                "Network": "In Network",
                "Amount": itemMax.get("FamilyAmount"),
                "Remaining": EligibilityPatientVerification.get("FamilyLifetimeRemainingBenefit"),
                "Used": itemMax.get("FamilyUsed"),
                "ServiceCategory": "Orthodontic",
                "BenefitPeriod": "",
                "Family_Individual": "Family"
            })


    temp = []
    frequencey = ""
    age = ""
    dental = ""
    covered = ""
    codeDes = ""
    code = ""
    Deductible = ""
    for benefits in EligibilityBenefitsData:
        temp.append(benefits)
        if benefits.get("Proccode",None):
            for sep in temp:
                if sep.get("Frequency",None):
                    frequencey = sep.get("Frequency")
                if sep.get("PercentCovered",None):
                    covered = sep.get("PercentCovered")
                if sep.get("Procedurecode",None):
                    codeDes = sep.get("Procedurecode")
                if sep.get("Age",None):
                    age = sep.get("Age")
                if sep.get("DentalArea",None):
                    dental = sep.get("DentalArea")
                if sep.get("Proccode",None):
                    code = sep.get("Proccode")
                if sep.get("IndividualDeductible",None):
                    Deductible = sep.get("IndividualDeductible")
                    if Deductible == "$0.00":
                        Deductible = "No"
                    else:
                        Deductible = "Yes"

            EligibilityBenefits.append({
                "ProcedureCode": code,
                "ProcedureCodeDescription": codeDes.replace(code.replace("D",""),"").strip(),
                "Amount": "",
                "Type": "",
                "limitation": frequencey+" "+age+" "+dental,
                "DeductibleApplies": Deductible,
                "Copay": "",
                "Benefits": covered
            })
            frequencey = ""
            age = ""
            dental = ""
            covered = ""
            codeDes = ""
            code = ""                       
            Deductible = ""
            temp = []

    type1 = ""
    type2 = ""
    for checkBen in EligibilityBenefits:
        DateService1 = ""
        DateService2 = ""
        for hist in TreatmentHistorySummaryData:
            type1 = hist.get("type").split(" ")[0].lower()
            type2 = hist.get("type").split("/")[0].lower()
            if search(type1, checkBen.get("ProcedureCodeDescription").lower()):
                DateService1 = hist.get("DateService1")
                DateService2 = hist.get("DateService2")
                break
            elif search(type2, checkBen.get("ProcedureCodeDescription").lower()):
                DateService1 = hist.get("DateService1")
                DateService2 = hist.get("DateService2")
                break
        EligibilityServiceTreatmentHistory.append({
            "ProcedureCode": checkBen.get("ProcedureCode"),
            "LimitationText": checkBen.get("limitation"),
            "History": str(DateService1+" "+DateService2).strip(),
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": checkBen.get("ProcedureCodeDescription")
        })
        TreatmentHistorySummary.append({
            "ProcedureCode": checkBen.get("ProcedureCode"),
            "LimitationText": checkBen.get("limitation"),
            "History": str(DateService1+" "+DateService2).strip(),
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": checkBen.get("ProcedureCodeDescription")
        })


    
    

    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\okalhama\SD%20Payor%20Scraping\okalhama.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\okalhama\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data, request)
# with open("OkalhamaOutput-BACON-GRAYSON.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
