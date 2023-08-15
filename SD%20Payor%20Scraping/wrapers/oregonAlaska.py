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
    EligibilityDeductiblesProcCodeData = Scraperdata.get("EligibilityDeductiblesProcCode")

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]

    EligibilityPatient = ""
    for item in EligibilityPatient1:
        if item.get("IdNumber", None):
            EligibilityPatient  = item
        if item.get("Gender",None):
            if item.get("Status") == "Active":
                EligibilityPatientVerification.update({"EligibilityStatus":"Active"})

            EligibilityPatientVerification.update({"Relationship":item.get("Relationship")})
            EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":item.get("BirthDate")})
            EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":item.get("PlanBegin")})
            EligibilityPatientVerification.update({"FamilyMemberEndDate":item.get("PlanEnd").replace("--/--/----","")})
            
            
            
            # EligibilityPatientVerification.update({"SubscriberEffectiveDate":item.get("CoverageEffectiveDate")})
            # EligibilityPatientVerification.update({"SubscriberEndDate":item.get("TermDate").replace("-","")})
    


    EligibilityPatientVerification.update({"SubscriberName":EligibilityPatient.get("SubscriberName")})
    EligibilityPatientVerification.update({"FamilyMemberName":patientdata.get("FirstName")+" "+patientdata.get("LastName")})
    EligibilityPatientVerification.update({"FamilyMemberId":patientdata.get("PatientMemberId")})
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate")})
    EligibilityPatientVerification.update({"PlanType":EligibilityPatient.get("InsuranceType")})
    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":EligibilityPatient.get("InsuranceType")})
    EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("GroupName")})
    EligibilityPatientVerification.update({"GroupNumber":EligibilityPatient.get("GroupNumber")})

    
    EligibilityPatientVerification.update({"InNetworkOutNetwork":"In Network"})
    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    #EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})

    EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":EligibilityPatient.get("DependentStopAge")})
    EligibilityPatientVerification.update({"DependentStudentAgeLimit":EligibilityPatient.get("StudentStopAge")})
    #EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":EligibilityPatient.get("WaitingPeriod")})
    EligibilityPatientVerification.update({"OrthodonticAgeLimits":EligibilityPatient.get("OrthoEligibility")})
    EligibilityPatientVerification.update({"ClaimMailingAddress":EligibilityTreatmentHistory[0].get("ClaimSubmissionAddress").replace("\n"," ")})
    EligibilityPatientVerification.update({"ClaimsAddress":EligibilityTreatmentHistory[0].get("ClaimSubmissionAddress").replace("\n"," ")})
    EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":EligibilityPatient.get("PolicyYear").replace("Service from/to date: ","")})

    
    
    # EligibilityPatientVerification.update({"MissingToothClause":EligibilityPatient.get("MissingToothClause")})
    # EligibilityPatientVerification.update({"CoordinationofBenefitsType":EligibilityPatient.get("CoordinaitonOfBenefit")})

    for items in EligibilityDeductiblesProcCodeData:
        if items.get("BasicRestorative", None):
            EligibilityPatientVerification.update({"AlternativeBenefitProvision":items.get("BasicRestorative")})

    

    ####----Maximums and deductibles-----###
    for itemMax in EligibilityMaximiums:
        if itemMax.get("Type",None):
            if "Deductible" in itemMax.get("Type"):
                EligibilityPatientVerification.update({"IndividualAnnualDeductible":itemMax.get("Individual")})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":itemMax.get("IndividualRemaining")})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining").strip())})
                EligibilityDeductiblesProcCode.append({
                    "Type": "Deductible",
                    "Network": "In Network",
                    "Amount": itemMax.get("Individual"),
                    "Remaining": itemMax.get("IndividualRemaining"),
                    "Used": EligibilityPatientVerification.get("IndividualAnnualDeductibleMet"),
                    "ServiceCategory": "",
                    "BenefitPeriod": "",
                    "Family_Individual": "Individual"
                })
                EligibilityPatientVerification.update({"FamilyAnnualDeductible":itemMax.get("Family")})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":itemMax.get("FamilyRemaining")})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualDeductible").strip(),EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining").strip())})
                EligibilityDeductiblesProcCode.append({
                    "Type": "Deductible",
                    "Network": "In Network",
                    "Amount": itemMax.get("Family"),
                    "Remaining": itemMax.get("FamilyRemaining"),
                    "Used": EligibilityPatientVerification.get("FamilyAnnualDeductibleMet"),
                    "ServiceCategory": "",
                    "BenefitPeriod": "",
                    "Family_Individual": "Family"
                })
            
            if "Annual" in itemMax.get("Type"):
                EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":itemMax.get("Individual")})
                EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":itemMax.get("IndividualRemaining")})
                EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit").strip())})
                EligibilityMaximums.append({
                    "Type": "Maximum",
                    "Network": "In Network",
                    "Amount": itemMax.get("Individual"),
                    "Remaining": itemMax.get("IndividualRemaining"),
                    "Used": EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate"),
                    "ServiceCategory": "",
                    "BenefitPeriod": "",
                    "Family_Individual": "Individual"
                })
                EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":itemMax.get("Family")})
                EligibilityPatientVerification.update({"FamilyAnnualRemainingBenefit":itemMax.get("FamilyRemaining")})
                EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("FamilyAnnualRemainingBenefit").strip())})
                EligibilityMaximums.append({
                    "Type": "Maximum",
                    "Network": "In Network",
                    "Amount": itemMax.get("Family"),
                    "Remaining": itemMax.get("FamilyRemaining"),
                    "Used": EligibilityPatientVerification.get("FamilyAnnualBenefitsUsedtoDate"),
                    "ServiceCategory": "",
                    "BenefitPeriod": "",
                    "Family_Individual": "Family"
                })


            if "Lifetime" in itemMax.get("Type"):
                EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":itemMax.get("Individual")})
                EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":itemMax.get("IndividualRemaining")})
                EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit").strip())})
                EligibilityMaximums.append({
                    "Type": "Lifetime",
                    "Network": "In Network",
                    "Amount": itemMax.get("Individual"),
                    "Remaining": itemMax.get("IndividualRemaining"),
                    "Used": EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate"),
                    "ServiceCategory": "",
                    "BenefitPeriod": "",
                    "Family_Individual": "Individual"
                })
                EligibilityPatientVerification.update({"FamilyLifetimeMaximumBenefits":itemMax.get("Family")})
                EligibilityPatientVerification.update({"FamilyLifetimeRemainingBenefit":itemMax.get("FamilyRemaining")})
                EligibilityPatientVerification.update({"FamilyLifetimeBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("FamilyLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("FamilyLifetimeRemainingBenefit").strip())})
                EligibilityMaximums.append({
                    "Type": "Lifetime",
                    "Network": "In Network",
                    "Amount": itemMax.get("Family"),
                    "Remaining": itemMax.get("FamilyRemaining"),
                    "Used": EligibilityPatientVerification.get("FamilyLifetimeBenefitsUsedtoDate"),
                    "ServiceCategory": "",
                    "BenefitPeriod": "",
                    "Family_Individual": "Family"
                })



    limitations = {
        "Bitewing xrays": "Bitewing xrays once in a calendar year",
        "Prophylaxis": "Prophylaxis or periodontal maintenance is covered twice in a calendar year",
        "Fluoride": "Fluoride is covered twice in a calendar year until the age of 19"
    }

    Codes ={
        "D9110":"Palliative Tx",
        "D0210":"FMX",
        "D0330":"Pano",
        "D1351":"Sealants",
        "D1354":"SDF",
        "D1516":"Space Maintainers",
        "D1517":"Space Maintainers",
        "D2140":"Amalgam Fillings- 1 Surface",
        "D2150":"Amalgam Fillings- 2 Surface",
        "D2160":"Amalgam Fillings- 3 Surface",
        "D2161":"Amalgam Fillings- 4 Surface",
        "D2391":"Composite Fillings- 1 Surface",
        "D2392":"Composite Fillings- 2 Surface",
        "D2393":"Composite Fillings- 3 Surface",
        "D2394":"Composite Fillings- 4 Surface",
        "D7140":"Routine Ext",
        "D3220":"Pulpotomy"
    }
    
    for benefits in EligibilityBenefitsData:
        if benefits.get("Proccode",None):
            agelimit = "MinimumAge:"+benefits.get("MinimumAge")+" and "+"MaximumAge:"+benefits.get("MiximumAge")

            BenefitPercent = ""
            deductiblesApplies = "No"
            frequency = ""
            Description = ""
            if benefits.get("ServiceType") != "":
                for deduct in EligibilityDeductiblesProcCodeData:
                    if deduct.get("ServiceType",None):
                        if benefits.get("ServiceType") in deduct.get("ServiceType"):
                            if deduct.get("Deductible",None):
                                if deduct.get("Deductible") == "":
                                    deductiblesApplies = "No"
                                else:
                                    deductiblesApplies = "Yes"
                            if deduct.get("BenefitPercent",None):
                                BenefitPercent = deduct.get("BenefitPercent")
                if "Bitewing X-rays" in benefits.get("ServiceType"):
                    frequency = limitations.get("Bitewing xrays")
                if "Prophylaxis" in benefits.get("ServiceType"):
                    frequency = limitations.get("Prophylaxis")
                if "Fluoride" in benefits.get("ServiceType"):
                    frequency = limitations.get("Fluoride")
            elif benefits.get("Description") == "":
                try:
                    Description = Codes.get(benefits.get("Proccode"))
                    for checkfreq in EligibilityDeductiblesProcCodeData:
                        if checkfreq.get("Preventive-P1",None):
                            for eachitem in checkfreq:
                                if Description.lower() in str(checkfreq.get(eachitem)).lower():
                                    frequency = checkfreq.get(eachitem)
                                    
                except:
                    pass

            EligibilityBenefits.append({
                "ProcedureCode": benefits.get("Proccode"),
                "ProcedureCodeDescription": benefits.get("Description")+str(Description),
                "Amount": "",
                "Type": benefits.get("ServiceType"),
                "limitation": str(frequency+", "+agelimit).strip(", "),
                "DeductibleApplies": deductiblesApplies,
                "Copay": "",
                "Benefits": BenefitPercent
            })

            EligibilityServiceTreatmentHistory.append({
                "ProcedureCode": benefits.get("Proccode"),
                "LimitationText": str(frequency+", "+agelimit).strip(", "),
                "History": benefits.get("BenefitNextAvailable").replace("--/--/----",""),
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": benefits.get("Description")+str(Description)
            })
            TreatmentHistorySummary.append({
                "ProcedureCode": benefits.get("Proccode"),
                "LimitationText": str(frequency+", "+agelimit).strip(", "),
                "History": benefits.get("BenefitNextAvailable").replace("--/--/----",""),
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": benefits.get("Description")+str(Description)
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

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\OregonAlaska\SD%20Payor%20Scraping\oregonAlaska.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\OregonAlaska\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data, request)
# with open("OreAlaskOutput-Alex-Montgomery.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
