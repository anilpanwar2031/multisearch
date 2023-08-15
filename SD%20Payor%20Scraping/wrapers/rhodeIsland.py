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
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")
    EligibilityDeductibles = Scraperdata.get("EligibilityDeductiblesProcCode")
    EligibilityTreatmentHistory = Scraperdata.get("EligibilityServiceTreatmentHistory")
    EligibilityOtherProvisions = Scraperdata.get("EligibilityOtherProvisions")


    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]



    EligibilityPatientVerification.update(
        {
        "FamilyMemberId":patientdata.get("SubscriberId"),
        "SubscriberId":patientdata.get("SubscriberId"),
        "SubscriberName":EligibilityPatient[0].get("SubscriberName"),
        # "InsuranceIDnumber":EligibilityPatient[0].get("InsurancePayerID"),
        "FamilyMemberName":EligibilityPatient[0].get("MemberName"),
        "FamilyMemberDateOfBirth":patientdata.get("BirthDate"),
        "Relationship":EligibilityPatient[0].get("Relationship"),
        "SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate"),
        "FamilyMemberEffectiveDate":EligibilityPatient[0].get("CoverageDate"),
        "FamilyMemberEndDate":EligibilityPatient[0].get("CoverageDate").split("-")[1].strip(),
        "InsuranceFeeScheduleUsed":EligibilityPatient[0].get("PlanType"),
        "GroupName":EligibilityPatient[0].get("GroupName"),
        "GroupNumber":EligibilityPatient[0].get("GroupNumber"),
        # "DependentStudentAgeLimit":EligibilityPatient[0].get("StudentAgeLimit:"),
        # "DependentChildCoveredAgeLimit":EligibilityPatient[0].get("DependentAgeLimit:"),
        "InsuranceCalendarOrFiscalPolicyYear":EligibilityPatient[0].get("CalendarYear"),
        "InNetworkOutNetwork":"In Network",
        "oonBenefits":"",
        # "CoordinationofBenefitsType":EligibilityPatient[0].get("CoordinationofBenefits"),
        # "CoordinationofBenefits":"Yes",
        # "AlternativeBenefitProvision":EligibilityPatient[0].get("AlternateBenefits:"),
        # "MissingToothClause":EligibilityPatient[0].get("MissingToothClause"),
        # "ClaimsAddress":EligibilityPatient[0].get("InsuranceMailingAddress"),
        # "ClaimMailingAddress":EligibilityPatient[0].get("InsuranceMailingAddress"),
         "PlanType":EligibilityPatient[0].get("PlanType")
        }
    )

    for other in EligibilityOtherProvisions:
        EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":other.get("DependentAge")})
        EligibilityPatientVerification.update({"MissingToothClause":other.get("MissingToothClause").replace("Note: ","")})
        EligibilityPatientVerification.update({"ClaimsAddress":other.get("mailingAddress").replace("\n"," ")})
        EligibilityPatientVerification.update({"ClaimMailingAddress":other.get("mailingAddress").replace("\n"," ")})
        EligibilityPatientVerification.update({"ClaimPayerID":other.get("payorID").replace("The Delta Dental payer ID number is ","").replace(".","")})

    if EligibilityPatient[0].get("CoverageDate",None):
         if search("Present",EligibilityPatient[0].get("CoverageDate")):
            EligibilityPatientVerification.update({"EligibilityStatus":"Active"})

    for item in EligibilityMaximiums:
        if item.get("Type") == "Individual Deductible":
            EligibilityPatientVerification.update({"IndividualAnnualDeductible":item.get("Amount")})
            EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":item.get("Remaining")})
            EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":item.get("Used")})
            EligibilityDeductiblesProcCode.append({
                "Type": "Deductible",
                "Network": "In Network",
                "Amount": item.get("Amount"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Used"),
                "ServiceCategory": "",
                "Family_Individual": "Individual"
            })
        elif item.get("Type") == "Family Deductible":
            EligibilityPatientVerification.update({"FamilyAnnualDeductible":item.get("Amount")})
            EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":item.get("Remaining")})
            EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":item.get("Used")})
            EligibilityDeductiblesProcCode.append({
                "Type": "Deductible",
                "Network": "In Network",
                "Amount": item.get("Amount"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Used"),
                "ServiceCategory": "",
                "Family_Individual": "Family"
            })
        elif item.get("Type") == "Annual Maximum":
            EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":item.get("Amount")})
            EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":item.get("Remaining")})
            EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":item.get("Used")})
            EligibilityMaximums.append({
                "Type": "Annual Maximum",
                "Network": "In Network",
                "Amount": item.get("Amount"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Used"),
                "ServiceCategory": "",
                "Family_Individual": "Individual"
            })
        elif search("Orthodontic Lifetime", str(item.get("Type"))):
            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":item.get("Amount")})
            EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":item.get("Remaining")})
            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":item.get("Used")})
            EligibilityMaximums.append({
                "Type": item.get("Type"),
                "Network": "In Network",
                "Amount": item.get("Amount"),
                "Remaining": item.get("Remaining"),
                "Used": item.get("Used"),
                "ServiceCategory": "Orthodontic",
                "Family_Individual": "Individual"
            })

    codes = [
        {"code":"D0150","search":"Oral exam"},
        {"code":"D0120","search":"Oral exam"},
        {"code":"D0140","search":"Oral exam"},
        {"code":"D0240","search":"Occlusal"},
        {"code":"D0272","search":"Bitewing x-rays"},
        {"code":"D0274","search":"Bitewing x-rays"},
        {"code":"D0210","search":"Complete x-ray series or panoramic film"},
        {"code":"D0330","search":"Complete x-ray series or panoramic film"},
        {"code":"D1110","search":"Cleaning"},
        {"code":"D1120","search":"Cleaning"},
        {"code":"D1206","search":"Fluoride treatment"},
        {"code":"D1208","search":"Fluoride treatment"},
        {"code":"D1351","search":"Sealants"},
        {"code":"D1354","search":"Other drugs and/or medicaments"},
        {"code":"D1516","search":"Space maintainers"},
        {"code":"D1517","search":"Space maintainers"},
        {"code":"D2140","search":"Amalgam (silver) fillings and composite (white) fillings"},
        {"code":"D2150","search":"Amalgam (silver) fillings and composite (white) fillings"},
        {"code":"D2160","search":"Amalgam (silver) fillings and composite (white) fillings"},
        {"code":"D2161","search":"Amalgam (silver) fillings and composite (white) fillings"},
        {"code":"D2391","search":"Amalgam (silver) fillings and composite (white) fillings"},
        {"code":"D2392","search":"Amalgam (silver) fillings and composite (white) fillings"},
        {"code":"D2393","search":"Amalgam (silver) fillings and composite (white) fillings"},
        {"code":"D2394","search":"Amalgam (silver) fillings and composite (white) fillings"},
        {"code":"D7140","search":"Extractions and other routine oral surgery"},
        {"code":"D2930","search":"Crowns over natural teeth, build ups, posts and cores"},
        {"code":"D2934","search":"Crowns over natural teeth, build ups, posts and cores"},
        {"code":"D9110","search":"Palliative"}
    ]

    for alterBenefit in EligibilityDeductibles:
        if "Amalgam (silver) fillings and composite (white) fillings" == alterBenefit.get("Procedure"):
            EligibilityPatientVerification.update({"AlternativeBenefitProvision":alterBenefit.get("Frequency/Limitations*")})
        if "Elective braces and related services" == alterBenefit.get("Procedure"):
            EligibilityPatientVerification.update({"OrthodonticAgeLimits":alterBenefit.get("Frequency/Limitations*")})

    for items in EligibilityBenefitsData:
        if items.get("Procedurecode") != "" and items.get("Procedurecode", None):
            limiation = ""
            for code in codes:
                if items.get("Procedurecode") == code.get("code"):
                    for searchItem in EligibilityDeductibles:
                        if code.get("search") == searchItem.get("Procedure") and searchItem.get("Procedure", None):
                            limiation = searchItem.get("Frequency/Limitations*")

            EligibilityBenefits.append({
                "ProcedureCode": items.get("Procedurecode"),
                "ProcedureCodeDescription": items.get("PrococdeDescription").replace("\u2013"," "),
                "Amount": "",
                "Type": "",
                "limitation": limiation,
                "DeductibleApplies": items.get("DeductibleApplies"),
                "Copay": "",
                "Benefits": items.get("CoveredAt"),
                "WaitingPeriod": items.get("WaitingPeriod")
            })

    for items in EligibilityBenefits:
        if items.get("ProcedureCode") != "" and items.get("ProcedureCode", None):
            History = ""
            ToothNumber = ""
            ToothSurface =""
            for hist in EligibilityTreatmentHistory:
                if items.get("ProcedureCode") == hist.get("ProcedureCode") and hist.get("ProcedureCode", None):
                    History = History +", "+ hist.get("ServiceDate")+" - "+hist.get("ToothNumber")+" - "+hist.get("ToothSurface")
                    ToothNumber = ToothNumber +", "+hist.get("ToothNumber")
                    ToothSurface = ToothSurface +", "+hist.get("ToothSurface")
            
            EligibilityServiceTreatmentHistory.append({
                "ProcedureCode": items.get("ProcedureCode"),
                "LimitationText": items.get("limitation"),
                "History": History.strip(', '),
                "Tooth": ToothNumber.strip(', ').replace("NA,","").replace("NA","").strip(),
                "Surface": ToothSurface.strip(', ').replace("NA,","").replace("NA","").strip(),
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": items.get("ProcedureCodeDescription")
            })
            TreatmentHistorySummary.append({
                "ProcedureCode": items.get("ProcedureCode"),
                "LimitationText": items.get("limitation"),
                "History": History.strip(', '),
                "Tooth": ToothNumber.strip(', ').replace("NA,","").replace("NA","").strip(),
                "Surface": ToothSurface.strip(', ').replace("NA,","").replace("NA","").strip(),
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": items.get("ProcedureCodeDescription")
            })

            if items.get("ProcedureCode") == "D2391":
               EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":items.get("WaitingPeriod")}) 


    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output







# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Rhode Island\SD%20Payor%20Scraping\rhodeIsland.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Rhode Island\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data, request)
# with open("RhodeIsland-Rehes-Jaden.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
