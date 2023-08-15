from mapPDF import mapEligibilityPatientVerification
from datetime import datetime
import json
from re import search
procCodeDesc=json.load(open("wrapers/procCodeDesc.json", 'r'))

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
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")[0]
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")
    EligibilityTreatmentHistory = Scraperdata.get("EligibilityServiceTreatmentHistory")
    EligibilityOtherProvisionsData = Scraperdata.get("EligibilityOtherProvisions")
    TreatmentHistorySummaryData = Scraperdata.get("TreatmentHistorySummary")
    EligibilityDeductiblesProcCodeData = Scraperdata.get("EligibilityDeductiblesProcCode")

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]

            
            
    if EligibilityPatient.get("Status") == "Active":
        EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
        EligibilityPatientVerification.update({"FamilyMemberName":EligibilityPatient.get("MemberName")})
        EligibilityPatientVerification.update({"FamilyMemberId":EligibilityPatient.get("MemberID")})
        EligibilityPatientVerification.update({"SubscriberId":EligibilityPatient.get("MemberID")})
        if "\n" in EligibilityPatient.get("GenderDOB"):
            EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":EligibilityPatient.get("GenderDOB").split("\n")[1]})
        if "\n" in EligibilityPatient.get("PayerGroupNbGrpNamPlanNb"):
            EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("PayerGroupNbGrpNamPlanNb").split("\n")[2]})
            EligibilityPatientVerification.update({"GroupNumber":EligibilityPatient.get("PayerGroupNbGrpNamPlanNb").split("\n")[1]})
            EligibilityPatientVerification.update({"PlanNumber":EligibilityPatient.get("PayerGroupNbGrpNamPlanNb").split("\n")[3]})
            EligibilityPatientVerification.update({"Payer":EligibilityPatient.get("PayerGroupNbGrpNamPlanNb").split("\n")[0]})
        if "\n" in EligibilityPatient.get("AlldetailsPlantype"):
            EligibilityPatientVerification.update({"PlanType":EligibilityPatient.get("AlldetailsPlantype").split("\n")[2]})
            EligibilityPatientVerification.update({"ProgramType":EligibilityPatient.get("AlldetailsPlantype").split("\n")[3]})
        if "\n" in EligibilityPatient.get("BeginAndEndDate"):
            EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":EligibilityPatient.get("BeginAndEndDate").split("\n")[0]})
        EligibilityPatientVerification.update({"ClaimMailingAddress":EligibilityPatient.get("ClaimAddressName")+", "+EligibilityPatient.get("ClaimAdressLine1")+", "+EligibilityPatient.get("ClaimAdressLine2")})
        EligibilityPatientVerification.update({"ClaimsAddress":EligibilityPatient.get("ClaimAddressName")+", "+EligibilityPatient.get("ClaimAdressLine1")+", "+EligibilityPatient.get("ClaimAdressLine2")})
        EligibilityPatientVerification.update({"SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName")})            
        EligibilityPatientVerification.update({"SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate")})
        EligibilityPatientVerification.update({"Relationship":patientdata.get("Relationship")})


        for itemMax in EligibilityMaximiums:
            try:
                if (itemMax.get("Coverage") == "Individual" and "In" in itemMax.get("Participation") and "$" in itemMax.get("CalenderYearAmount")):
                    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":itemMax.get("CalenderYearAmount")})
                    EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":itemMax.get("RemainingAmount")})
                    EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit").strip())})
                    EligibilityMaximums.append({
                        "Type": "Maximum",
                        "Network": itemMax.get("Participation"),
                        "Amount": itemMax.get("CalenderYearAmount"),
                        "Remaining": itemMax.get("RemainingAmount"),
                        "Used": EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate"),
                        "ServiceCategory": itemMax.get("Message"),
                        "BenefitPeriod": "",
                        "Family_Individual": "Individual"
                    })
                    break
            except:
                pass

        for itemMax in EligibilityMaximiums:
            try:
                if (itemMax.get("Participation") == "In- and Out- of Network"):
                    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
                if ("In" in itemMax.get("Participation")):
                    EligibilityPatientVerification.update({"InNetworkOutNetwork":"In Network"})
            except:
                pass


        for itemDeduct in EligibilityDeductiblesProcCodeData:
            try:
                if ("$" in itemDeduct.get("CalenderYearAmount") and "In" in itemDeduct.get("Participation")):
                    EligibilityPatientVerification.update({"IndividualAnnualDeductible":itemDeduct.get("CalenderYearAmount")})
                    EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":itemDeduct.get("RemainingAmount")})
                    EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining").strip())})
                    EligibilityDeductiblesProcCode.append({
                        "Type": "Maximum",
                        "Network": itemDeduct.get("Participation"),
                        "Amount": itemDeduct.get("CalenderYearAmount"),
                        "Remaining": itemDeduct.get("RemainingAmount"),
                        "Used": EligibilityPatientVerification.get("IndividualAnnualDeductibleMet"),
                        "ServiceCategory": itemDeduct.get("Message"),
                        "BenefitPeriod": "",
                        "Family_Individual": "Individual"
                    })
                    break
            except:
                pass

        for itemDeduct2 in EligibilityDeductiblesProcCodeData:
            try:
                if ("$" in itemDeduct2.get("FamilyCalenderYearAmount") and "In" in itemDeduct2.get("Participation")):
                    EligibilityPatientVerification.update({"FamilyAnnualDeductible":itemDeduct2.get("FamilyCalenderYearAmount")})
                    EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":itemDeduct2.get("FamilyRemainingAmount")})
                    EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualDeductible").strip(),EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining").strip())})
                    EligibilityDeductiblesProcCode.append({
                        "Type": "Maximum",
                        "Network": itemDeduct2.get("Participation"),
                        "Amount": itemDeduct2.get("FamilyCalenderYearAmount"),
                        "Remaining": itemDeduct2.get("FamilyRemainingAmount"),
                        "Used": EligibilityPatientVerification.get("FamilyAnnualDeductibleMet"),
                        "ServiceCategory": itemDeduct2.get("Message"),
                        "BenefitPeriod": "",
                        "Family_Individual": "Family"
                    })
                    break
            except:
                pass


        for itemBenefit in EligibilityBenefitsData:
            if(itemBenefit.get("LimitationMaximum")=="" and itemBenefit.get("Coinsurance")=="" and itemBenefit.get("DeductiblesInformation")=="" and itemBenefit.get("BenefitDescription")==""):
                for itemProvision in EligibilityOtherProvisionsData:
                    if itemBenefit.get("Proccode") == itemProvision.get("Proccode"):
                        itemBenefit["LimitationMaximum"] = itemProvision.get("LimitationMaximum")
                        itemBenefit["Coinsurance"] = itemProvision.get("Coinsurance")
                        itemBenefit["DeductiblesInformation"] = itemProvision.get("DeductiblesInformation")
                        itemBenefit["BenefitDescription"] = itemProvision.get("BenefitDescription")
                        break

        
        for benefits in EligibilityBenefitsData:
            Coinsurance = ""
            DeductiblesInformation = ""
            Limitation = ""
            History = ""
            Childage = ""
            StudentAge = ""
            MaximumAge = ""
            ProcedureCodeDescription = ""
            if procCodeDesc.get(benefits.get("Proccode")):
                ProcedureCodeDescription = procCodeDesc.get(benefits.get("Proccode"))
            if ("%" in benefits.get("Coinsurance") and benefits.get("Proccode") in benefits.get("Coinsurance")):
                Coinsurance = benefits.get("Coinsurance").split(benefits.get("Proccode"))[1].split("%")[0].strip()
                Coinsurance = str(100-int(Coinsurance))+"%"

            if ("$" in benefits.get("DeductiblesInformation") and  "In" in benefits.get("DeductiblesInformation")):
                DeductiblesInformation = "Yes"
            elif ("DEDUCTIBLE DOES NOT APPLY" in benefits.get("LimitationMaximum")):
                DeductiblesInformation = "No"

            if ("Visit" in benefits.get("LimitationMaximum") or "Unit" in benefits.get("LimitationMaximum")):
                LimitationArry = benefits.get("LimitationMaximum").split(benefits.get("Proccode"))
                for itemLimation in LimitationArry:
                    if ("Visit" in itemLimation or "Unit" in itemLimation):
                        Limitation = itemLimation.replace("\n","")
                        break
                if "Network" in Limitation:
                    Limitation = Limitation.split("Network")[1].strip()
                    if ("Year" in Limitation):
                        Limitation = Limitation.split("Year")[0].strip()+" Year"
                    elif ("Years" in Limitation):
                        Limitation = Limitation.split("Years")[0].strip()+" Years"
                    elif ("Month" in Limitation):
                        Limitation = Limitation.split("Month")[0].strip()+" Month"
                    elif ("Months" in Limitation):
                        Limitation = Limitation.split("Months")[0].strip()+" Months"

            if "Age" in benefits.get("LimitationMaximum"):
                ageArrayAll = benefits.get("LimitationMaximum").split(benefits.get("Proccode"))
                for ageitems in ageArrayAll:
                    if "Age" in ageitems:
                        agearray = ageitems.split(" ")
                        for finalage in agearray:
                            if "Age" in finalage:
                                MaximumAge = " Maximum "+finalage.replace("\n","")
                                break
                        break


            if ("Last paid date" in benefits.get("LimitationMaximum")):
                HistoryAll = benefits.get("LimitationMaximum").split(benefits.get("Proccode"))
                for hist in HistoryAll:
                    if "Last paid date" in hist:
                        History = hist.split("Last paid date")[1].replace("\n","").strip()
                        break

            if ("CHLD" in benefits.get("LimitationMaximum") or "STUDENT" in benefits.get("LimitationMaximum")):
                All = benefits.get("LimitationMaximum").split(benefits.get("Proccode"))
                for hist in All:
                    if ("CHLD" in hist or "STUDENT" in hist):
                        try:
                            Childage = hist.split(",")[1].split("OR")[0]
                            EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":Childage})
                        except:
                            pass
                        try:
                            StudentAge = hist.split(",")[1].split("OR")[1]
                            EligibilityPatientVerification.update({"DependentStudentAgeLimit":StudentAge})
                        except:
                            pass
                        break
            

            EligibilityBenefits.append({
                "ProcedureCode": benefits.get("Proccode"),
                "ProcedureCodeDescription": ProcedureCodeDescription,
                "Amount": "",
                "Type": "",
                "limitation": Limitation+MaximumAge,
                "DeductibleApplies": DeductiblesInformation,
                "Copay": "",
                "Benefits": Coinsurance
            })

            if(History != ""):
                EligibilityServiceTreatmentHistory.append({
                    "ProcedureCode": benefits.get("Proccode"),
                    "LimitationText": Limitation,
                    "History": History,
                    "Tooth": "",
                    "Surface": "",
                    "LimitationAlsoAppliesTo": "",
                    "ProcedureCodeDescription": ProcedureCodeDescription
                })
                TreatmentHistorySummary.append({
                    "ProcedureCode": benefits.get("Proccode"),
                    "LimitationText": Limitation,
                    "History": History,
                    "Tooth": "",
                    "Surface": "",
                    "LimitationAlsoAppliesTo": "",
                    "ProcedureCodeDescription": ProcedureCodeDescription
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

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Aetna\on dev\SD%20Payor%20Scraping\aetnaPP.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Aetna\on dev\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data, request)
# with open("AetnaPatient.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
