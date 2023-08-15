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

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]

    EligibilityPatient = ""
    for item in EligibilityPatient1:
        if item.get("Subscriber", None):
            EligibilityPatient  = item
        if item.get("Name",None):
            if item.get("Birthdate") == patientdata.get("BirthDate"):
                if item.get("TerminationDate") == "Active":
                    EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
                EligibilityPatientVerification.update({"Relationship":item.get("Relationship")})
                EligibilityPatientVerification.update({"FamilyMemberName":item.get("Name")})            
                EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":item.get("Birthdate")})
                EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":item.get("EffectiveDate")})
                EligibilityPatientVerification.update({"FamilyMemberEndDate":item.get("TerminationDate")})
            if item.get("Relationship") == "Subscriber":
                EligibilityPatientVerification.update({"SubscriberName":item.get("Name")})            
                EligibilityPatientVerification.update({"SubscriberDateOfBirth":item.get("Birthdate")})
                EligibilityPatientVerification.update({"SubscriberEffectiveDate":item.get("EffectiveDate")})
                EligibilityPatientVerification.update({"SubscriberEndDate":item.get("TerminationDate")})
                if item.get("TerminationDate") == "Active":
                    EligibilityPatientVerification.update({"SubscriberEligibilityStatus":"Active"})
            
            

    


    EligibilityPatientVerification.update({"FamilyMemberId":EligibilityPatient.get("subID")})
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"PlanType":EligibilityPatient.get("product")})
    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":EligibilityPatient.get("product")})
    EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("GroupName")})
    EligibilityPatientVerification.update({"GroupNumber":EligibilityPatient.get("GroupNumber")})

    
    EligibilityPatientVerification.update({"InNetworkOutNetwork":"In Network"})
    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":EligibilityPatient.get("DependentAge")})
    EligibilityPatientVerification.update({"DependentStudentAgeLimit":EligibilityPatient.get("studentAge")})
    # #EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":EligibilityPatient.get("WaitingPeriod")})
    EligibilityPatientVerification.update({"OrthodonticAgeLimits":EligibilityPatient.get("OrthoAge")})
    # # EligibilityPatientVerification.update({"MissingToothClause":EligibilityPatient.get("MissingToothClause")})
    # # EligibilityPatientVerification.update({"CoordinationofBenefitsType":EligibilityPatient.get("CoordinaitonOfBenefit")})

    for items in EligibilityDeductiblesProcCodeData:
        if items.get("BenefitPeriod", None):
            EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":items.get("BenefitPeriod").replace("Benefit Period: ","")})

    try:
        if "coordination of benefits" and "\n" in EligibilityPatient.get("CoordinaitonBenefit"):
            coordinationOfBenefit = EligibilityPatient.get("CoordinaitonBenefit").split("\n")[0].replace("\u2022","").strip()
            MedicallyNecessaryonly = EligibilityPatient.get("CoordinaitonBenefit").split("\n")[1].replace("\u2022","").strip()
            EligibilityPatientVerification.update({"CoordinationofBenefits":coordinationOfBenefit})
            EligibilityPatientVerification.update({"MedicallyNecessaryonly":MedicallyNecessaryonly})
    except:
        pass

    
    if "Phone" in TreatmentHistorySummaryData[0].get("claimAddress"):
        claimAddress = TreatmentHistorySummaryData[0].get("claimAddress").split("Phone")[0].replace("\n"," ")
        EligibilityPatientVerification.update({"ClaimMailingAddress":claimAddress})
        EligibilityPatientVerification.update({"ClaimsAddress":claimAddress})
    
    
    
    ####----Maximums and deductibles-----###
    for itemMax in EligibilityMaximiums:
        if itemMax.get("type",None):
            if "All Covered Classes" in itemMax.get("classes") and "Individual" in itemMax.get("type"):
                EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":itemMax.get("total").replace("\nper year,","")})
                EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":itemMax.get("remaining").replace(" remaining","")})
                EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit").strip())})
                EligibilityMaximums.append({
                    "Type": "Maximum",
                    "Network": "In Network",
                    "Amount": itemMax.get("total").replace("\nper year,",""),
                    "Remaining": itemMax.get("remaining").replace(" remaining",""),
                    "Used": EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate"),
                    "ServiceCategory": itemMax.get("classes"),
                    "BenefitPeriod": EligibilityPatientVerification.get("InsuranceCalendarOrFiscalPolicyYear"),
                    "Family_Individual": "Individual"
                })
            if "Orthodontics" in itemMax.get("classes") and "Individual" in itemMax.get("type"):
                EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":itemMax.get("total").replace("\nlifetime,","")})
                EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":itemMax.get("remaining").replace(" remaining","")})
                EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":calculate_difference(EligibilityPatientVerification.get("OrthodonticLifetimeBenefit").strip(),EligibilityPatientVerification.get("OrthodonticLifetimeRemainingBenefit").strip())})
                
                EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":itemMax.get("total").replace("\nlifetime,","")})
                EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":itemMax.get("remaining").replace(" remaining","")})
                EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit").strip())})
                EligibilityMaximums.append({
                    "Type": "Lifetime Maximum",
                    "Network": "In Network",
                    "Amount": itemMax.get("total").replace("\nlifetime,",""),
                    "Remaining": itemMax.get("remaining").replace(" remaining",""),
                    "Used": EligibilityPatientVerification.get("OrthodonticLifetimeBenefitUsedtoDate"),
                    "ServiceCategory": itemMax.get("classes"),
                    "BenefitPeriod": EligibilityPatientVerification.get("InsuranceCalendarOrFiscalPolicyYear"),
                    "Family_Individual": "Individual"
                })


    for itemMax in EligibilityDeductiblesProcCodeData:
        if itemMax.get("type",None):
            if "All Covered Classes" in itemMax.get("classes") and "Individual" in itemMax.get("type"):
                EligibilityPatientVerification.update({"IndividualAnnualDeductible":itemMax.get("total").replace("\nper year,","")})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":itemMax.get("remaining").replace(" remaining","")})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining").strip())})
                EligibilityDeductiblesProcCode.append({
                    "Type": "Deductible",
                    "Network": "In Network",
                    "Amount": itemMax.get("total").replace("\nper year,",""),
                    "Remaining": itemMax.get("remaining").replace(" remaining",""),
                    "Used": EligibilityPatientVerification.get("IndividualAnnualDeductibleMet"),
                    "ServiceCategory": itemMax.get("classes"),
                    "BenefitPeriod": EligibilityPatientVerification.get("InsuranceCalendarOrFiscalPolicyYear"),
                    "Family_Individual": "Individual"
                })
            if "All Covered Classes" in itemMax.get("classes") and "Family" in itemMax.get("type"):
                EligibilityPatientVerification.update({"FamilyAnnualDeductible":itemMax.get("total").replace("\nper year,","")})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":itemMax.get("remaining").replace(" remaining","")})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualDeductible").strip(),EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining").strip())})
                EligibilityDeductiblesProcCode.append({
                    "Type": "Deductible",
                    "Network": "In Network",
                    "Amount": itemMax.get("total").replace("\nper year,",""),
                    "Remaining": itemMax.get("remaining").replace(" remaining",""),
                    "Used": EligibilityPatientVerification.get("FamilyAnnualDeductibleMet"),
                    "ServiceCategory": itemMax.get("classes"),
                    "BenefitPeriod": EligibilityPatientVerification.get("InsuranceCalendarOrFiscalPolicyYear"),
                    "Family_Individual": "Family"
                })


    #GetCodesDeductiblesApply-percentBenefit-type#
    deductApplyDetails = []
    codesDetails = []
    index = 0
    for codesBenefits in EligibilityTreatmentHistory[1:]:
        if codesBenefits.get("WaitingPeriod",None):
            if "Delta Dental PPO" in codesBenefits.get("WaitingPeriod"):
                break
        if codesBenefits.get("WaitingPeriod",None):
            deductApplyDetails.append(codesBenefits)
        if not codesBenefits.get("WaitingPeriod",None):
            codesDetails.append(codesBenefits)
        index = index + 1
    
    mergeDeductApplyDetailsAndCodes = []

    for i in range(0,len(deductApplyDetails)):
        mergeDeductApplyDetailsAndCodes.append(deductApplyDetails[i])
        mergeDeductApplyDetailsAndCodes[i].update({"codesDetail":codesDetails[i].get("ServiceType")})

    
    ExceptionCodes = []
    for i in range(index,len(EligibilityTreatmentHistory)):
        ExceptionCodes.append(EligibilityTreatmentHistory[i])
    #GetCodesDeductiblesApply-percentBenefit-type#

    
    
    
    
    limitationdetails = []
    codeDetailsLimitation = []
    count = 0
    for limitdetails in EligibilityOtherProvisionsData:
        if "Procedure Exceptions" in limitdetails.get("ServiceType"):
            break
        if limitdetails.get("Frequency",None):
            limitationdetails.append(limitdetails)
        if not limitdetails.get("Frequency",None):
            codeDetailsLimitation.append(limitdetails)
        count = count + 1

    mergeLimitationAndCode = []
    for i in range(0,len(limitationdetails)):
        mergeLimitationAndCode.append(limitationdetails[i])
        mergeLimitationAndCode[i].update({"codesDetail":codeDetailsLimitation[i].get("ServiceType")})

    
    ExceptionLimitation = []
    for i in range(count,len(EligibilityOtherProvisionsData)):
        ExceptionLimitation.append(EligibilityOtherProvisionsData[i])

    






    #Eligibility Benefits#
    for benefits in EligibilityBenefitsData:
        frequency = benefits.get("Frequency")
        agelimit = "Age Limit: "+benefits.get("AgeLimitLow")+" - "+benefits.get("AgeLimitHigh")
        ServiceType = ""
        WaitingPeriod = ""
        PPOpatientPays = ""
        PPODeductibles = ""
        limitation = ""
        for getcode in mergeDeductApplyDetailsAndCodes:
            if benefits.get("code") in getcode.get("codesDetail") and benefits.get("code") != "":
                ServiceType = getcode.get("ServiceType")
                WaitingPeriod = getcode.get("WaitingPeriod")
                PPOpatientPays = getcode.get("PPOpatientPays")
                PPODeductibles = getcode.get("PPODeductibles")
                break
        if ServiceType == "":
            for getcodeExcep in ExceptionCodes[3:]:
                if benefits.get("code") in getcodeExcep.get("ServiceType") and benefits.get("code") != "":
                    WaitingPeriod = getcodeExcep.get("WaitingPeriod")
                    PPOpatientPays = getcodeExcep.get("PPOpatientPays")
                    PPODeductibles = getcodeExcep.get("PPODeductibles")
                    break            

        for getlimitation in mergeLimitationAndCode:
            if benefits.get("code") in getlimitation.get("codesDetail") and benefits.get("code") != "":
                limitation = getlimitation.get("limitation")
        if limitation == "":
            for getlimitationExcept in ExceptionLimitation[1:]:
                if benefits.get("code") in getlimitationExcept.get("ServiceType") and benefits.get("code") != "":
                    limitation = getlimitationExcept.get("limitation")


        if benefits.get("Proccode") == "2391":
            #EligibilityPatientVerification.update({"AlternativeBenefitProvision":str(limitation+", "+frequency+", "+agelimit+", Waiting Period: "+WaitingPeriod).strip(", ")})
            EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":WaitingPeriod})

        if PPOpatientPays != "":
            PPOpatientPays = str(100 - int(PPOpatientPays.replace("%","")))+"%"
        
        EligibilityBenefits.append({
            "ProcedureCode": "D"+benefits.get("Proccode"),
            "ProcedureCodeDescription": str(ServiceType+", "+benefits.get("Description")).strip(", "),
            "Amount": "",
            "Type": ServiceType,
            "limitation": str(limitation+", "+frequency+", "+agelimit+", Waiting Period: "+WaitingPeriod).strip(", "),
            "DeductibleApplies": PPODeductibles,
            "Copay": "",
            "Benefits": PPOpatientPays
        })

        EligibilityServiceTreatmentHistory.append({
            "ProcedureCode": "D"+benefits.get("Proccode"),
            "LimitationText": str(limitation+", "+frequency+", "+agelimit+", Waiting Period: "+WaitingPeriod).strip(", "),
            "History": benefits.get("History").replace("\n",", "),
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": benefits.get("RelatedCodes"),
            "ProcedureCodeDescription": str(ServiceType+", "+benefits.get("Description")).strip(", ")
        })
        TreatmentHistorySummary.append({
            "ProcedureCode": "D"+benefits.get("Proccode"),
            "LimitationText": str(limitation+", "+frequency+", "+agelimit+", Waiting Period: "+WaitingPeriod).strip(", "),
            "History": benefits.get("History").replace("\n",", "),
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": benefits.get("RelatedCodes"),
            "ProcedureCodeDescription": str(ServiceType+", "+benefits.get("Description")).strip(", ")
        })

    # limitations = {
    #     "Bitewing xrays": "Bitewing xrays once in a calendar year",
    #     "Prophylaxis": "Prophylaxis or periodontal maintenance is covered twice in a calendar year",
    #     "Fluoride": "Fluoride is covered twice in a calendar year until the age of 19"
    # }

    # Codes ={
    #     "D9110":"Palliative Tx",
    #     "D0210":"FMX",
    #     "D0330":"Pano",
    #     "D1351":"Sealants",
    #     "D1354":"SDF",
    #     "D1516":"Space Maintainers",
    #     "D1517":"Space Maintainers",
    #     "D2140":"Amalgam Fillings- 1 Surface",
    #     "D2150":"Amalgam Fillings- 2 Surface",
    #     "D2160":"Amalgam Fillings- 3 Surface",
    #     "D2161":"Amalgam Fillings- 4 Surface",
    #     "D2391":"Composite Fillings- 1 Surface",
    #     "D2392":"Composite Fillings- 2 Surface",
    #     "D2393":"Composite Fillings- 3 Surface",
    #     "D2394":"Composite Fillings- 4 Surface",
    #     "D7140":"Routine Ext",
    #     "D3220":"Pulpotomy"
    # }
    
    # for benefits in EligibilityBenefitsData:
    #     if benefits.get("Proccode",None):
    #         agelimit = "MinimumAge:"+benefits.get("MinimumAge")+" and "+"MaximumAge:"+benefits.get("MiximumAge")

    #         BenefitPercent = ""
    #         deductiblesApplies = "No"
    #         frequency = ""
    #         Description = ""
    #         if benefits.get("ServiceType") != "":
    #             for deduct in EligibilityDeductiblesProcCodeData:
    #                 if deduct.get("ServiceType",None):
    #                     if benefits.get("ServiceType") in deduct.get("ServiceType"):
    #                         if deduct.get("Deductible",None):
    #                             if deduct.get("Deductible") == "":
    #                                 deductiblesApplies = "No"
    #                             else:
    #                                 deductiblesApplies = "Yes"
    #                         if deduct.get("BenefitPercent",None):
    #                             BenefitPercent = deduct.get("BenefitPercent")
    #             if "Bitewing X-rays" in benefits.get("ServiceType"):
    #                 frequency = limitations.get("Bitewing xrays")
    #             if "Prophylaxis" in benefits.get("ServiceType"):
    #                 frequency = limitations.get("Prophylaxis")
    #             if "Fluoride" in benefits.get("ServiceType"):
    #                 frequency = limitations.get("Fluoride")
    #         elif benefits.get("Description") == "":
    #             try:
    #                 Description = Codes.get(benefits.get("Proccode"))
    #                 for checkfreq in EligibilityDeductiblesProcCodeData:
    #                     if checkfreq.get("Preventive-P1",None):
    #                         for eachitem in checkfreq:
    #                             if Description.lower() in str(checkfreq.get(eachitem)).lower():
    #                                 frequency = checkfreq.get(eachitem)
                                    
    #             except:
    #                 pass

    #         EligibilityBenefits.append({
    #             "ProcedureCode": benefits.get("Proccode"),
    #             "ProcedureCodeDescription": benefits.get("Description")+str(Description),
    #             "Amount": "",
    #             "Type": benefits.get("ServiceType"),
    #             "limitation": str(frequency+", "+agelimit).strip(", "),
    #             "DeductibleApplies": deductiblesApplies,
    #             "Copay": "",
    #             "Benefits": BenefitPercent
    #         })

    #         EligibilityServiceTreatmentHistory.append({
    #             "ProcedureCode": benefits.get("Proccode"),
    #             "LimitationText": str(frequency+", "+agelimit).strip(", "),
    #             "History": benefits.get("BenefitNextAvailable").replace("--/--/----",""),
    #             "Tooth": "",
    #             "Surface": "",
    #             "LimitationAlsoAppliesTo": "",
    #             "ProcedureCodeDescription": benefits.get("Description")+str(Description)
    #         })
    #         TreatmentHistorySummary.append({
    #             "ProcedureCode": benefits.get("Proccode"),
    #             "LimitationText": str(frequency+", "+agelimit).strip(", "),
    #             "History": benefits.get("BenefitNextAvailable").replace("--/--/----",""),
    #             "Tooth": "",
    #             "Surface": "",
    #             "LimitationAlsoAppliesTo": "",
    #             "ProcedureCodeDescription": benefits.get("Description")+str(Description)
    #         })
        




    
    

    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Maine, New Hampshire, Vermont\deployment\SD%20Payor%20Scraping\maineHempshireVermont.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Maine, New Hampshire, Vermont\deployment\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data, request)
# with open("maineHempshireVermont-Braylee-Harris.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
