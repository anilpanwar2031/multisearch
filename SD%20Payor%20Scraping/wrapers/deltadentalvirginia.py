from mapPDF import mapEligibilityPatientVerification
from datetime import datetime
import json
from re import search
procCodeDesc=json.load(open("wrapers/procCodeDesc.json", 'r'))
from FileDownload import Downloader
import random,string
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

def ScrapePDF(Scraperdata):
    file_path =''.join(random.choices(string.ascii_uppercase +string.digits, k=10)) + ".pdf"
    input_file = Scraperdata["EligibilityPatientVerification"][0]["url"][0].replace("%20", " ")

    Downloader('Eligibility',file_path,input_file)

    df = tabula.read_pdf(file_path, 
                     guess=False, pages='1', stream=True , encoding="utf-8", 
                     area = (245.95837045669555,23.715, 726.3783704566956,582.165))

    df=df[0]
    df =df.set_axis(["key","value"], axis=1)
    json_data =dict(zip(df['key'], df['value']))

    df_address = tabula.read_pdf(file_path, 
                     guess=False, pages='1', stream=True , encoding="utf-8", 
                     area = (70.7625,29.681990661621093, 158.7375,243.1169906616211))
    
    addr = ' '.join(df_address[0]['Delta Dental of Virginia'].to_list())
    addr = f'Delta Dental of Virginia {addr}'
    add = df_address[0]['Delta Dental of Virginia'].to_list()
    json_data['electronic_payer_id'] = add.pop(-1).split(':')[-1].strip()
    json_data['address'] = f"Delta Dental of Virginia {' '.join(add[:-1])}"  

    # print(json_data['electronic_payer_id'])    
    
    
    Scraperdata["EligibilityPatientVerification"][0].update(
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

    return Scraperdata

def main(Scraperdata, request):
    pdf_data = ScrapePDF(Scraperdata)

    patientdata = request.get("PatientData")[0]
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")[0]
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")[0]
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

            

    EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
    EligibilityPatientVerification.update({"FamilyMemberName":EligibilityPatient.get("PatienName")})
    EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("GroupName")})
    EligibilityPatientVerification.update({"GroupNumber":EligibilityPatient.get("GroupNumber")})
    EligibilityPatientVerification.update({"PlanType":EligibilityPatient.get("Product")})
    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":EligibilityPatient.get("Product")})
    EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":EligibilityPatient.get("EffectiveDate")})
    EligibilityPatientVerification.update({"FamilyMemberEndDate":EligibilityPatient.get("TerminateDate")})
    EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":EligibilityPatient.get("BenefitPeriod")})
    EligibilityPatientVerification.update({"InNetworkOutNetwork":"In Network"})
    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    ##pdfdata##
    EligibilityPatientVerification.update({"CoordinationofBenefitsType":EligibilityPatient.get("CoordinationofBenefits")})
    EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})
    EligibilityPatientVerification.update({"AlternativeBenefitProvision":EligibilityPatient.get("AlternateBenefits")})
    EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":EligibilityPatient.get("DependentAgeLimit")})
    EligibilityPatientVerification.update({"DependentStudentAgeLimit":EligibilityPatient.get("StudentAgeLimit")})
    EligibilityPatientVerification.update({"OrthodonticAgeLimits":EligibilityPatient.get("OrthodonticAgeMinMax")})
    EligibilityPatientVerification.update({"ClaimsAddress":EligibilityPatient.get("Claimaddress")})
    EligibilityPatientVerification.update({"ClaimMailingAddress":EligibilityPatient.get("Claimaddress")})
    EligibilityPatientVerification.update({"ClaimPayerID":EligibilityPatient.get("electronicpayer_id")})
    ##pdfdata##


    EligibilityPatientVerification.update({"FamilyMemberId":patientdata.get("PatientMemberId")})
    EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":patientdata.get("BirthDate")})
    EligibilityPatientVerification.update({"Relationship":patientdata.get("Relationship")})
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate")})
    EligibilityPatientVerification.update({"SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName")})



    #Maximums and deductibles
    benefitsAll = EligibilityMaximiums.get("BenefitAll")
    if "Out of Network" in benefitsAll:
        benefitsItems = benefitsAll.split("Out of Network")
        for items in benefitsItems:
            if "Individual Calendar Year Maximum (PPO)" in items:
                overallBenefits = items.split("(PPO)")[1].split("Total allowed:")
                totals = overallBenefits[1]
                if "\n" in totals:
                    totals = totals.split("\n")[0].strip()
                else:
                    totals = overallBenefits[1].replace("\n","").strip()
                usedAndRemaining = overallBenefits[0].split("/")
                used = usedAndRemaining[0].replace("Used:","").replace("\n","").strip()
                remaining = usedAndRemaining[1].replace("Remaining:","").replace("\n","").strip()
                EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":totals})
                EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":remaining})
                EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":used})
                EligibilityMaximums.append({
                    "Type": "Individual Calendar Year Maximum",
                    "Network": "In Network",
                    "Amount": totals,
                    "Remaining": remaining,
                    "Used": used,
                    "ServiceCategory": "",
                    "BenefitPeriod": EligibilityPatientVerification.get("InsuranceCalendarOrFiscalPolicyYear"),
                    "Family_Individual": "Individual"
                })

            if (("Ortho Lifetime Maximum (PPO)" in items or "Orthodontic Lifetime Maximum (PPO)" in items) and "Individual" in items):
                overallBenefits = items.split("(PPO)")[1].split("Total allowed:")
                totals = overallBenefits[1]
                if "\n" in totals:
                    totals = totals.split("\n")[0].strip()
                else:
                    totals = overallBenefits[1].replace("\n","").strip()
                usedAndRemaining = overallBenefits[0].split("/")
                used = usedAndRemaining[0].replace("Used:","").replace("\n","").strip()
                remaining = usedAndRemaining[1].replace("Remaining:","").replace("\n","").strip()
                EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":totals})
                EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":remaining})
                EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":used})
                EligibilityMaximums.append({
                    "Type": "Individual Ortho Lifetime Maximum",
                    "Network": "In Network",
                    "Amount": totals,
                    "Remaining": remaining,
                    "Used": used,
                    "ServiceCategory": "",
                    "BenefitPeriod": EligibilityPatientVerification.get("InsuranceCalendarOrFiscalPolicyYear"),
                    "Family_Individual": "Individual"
                })

            if "Family Annual Deductible (PPO)" in items:
                overallBenefits = items.split("(PPO)")[1].split("Total allowed:")
                totals = overallBenefits[1]
                if "\n" in totals:
                    totals = totals.split("\n")[0].strip()
                else:
                    totals = overallBenefits[1].replace("\n","").strip()
                usedAndRemaining = overallBenefits[0].split("/")
                used = usedAndRemaining[0].replace("Used:","").replace("\n","").strip()
                remaining = usedAndRemaining[1].replace("Remaining:","").replace("\n","").strip()
                EligibilityPatientVerification.update({"FamilyAnnualDeductible":totals})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":remaining})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":used})
                EligibilityDeductiblesProcCode.append({
                    "Type": "Family Annual Deductible",
                    "Network": "In Network",
                    "Amount": totals,
                    "Remaining": remaining,
                    "Used": used,
                    "ServiceCategory": "",
                    "BenefitPeriod": EligibilityPatientVerification.get("InsuranceCalendarOrFiscalPolicyYear"),
                    "Family_Individual": "Family"
                })

            if "Individual Annual Deductible (PPO)" in items:
                overallBenefits = items.split("(PPO)")[1].split("Total allowed:")
                totals = overallBenefits[1]
                if "\n" in totals:
                    totals = totals.split("\n")[0].strip()
                else:
                    totals = overallBenefits[1].replace("\n","").strip()
                usedAndRemaining = overallBenefits[0].split("/")
                used = usedAndRemaining[0].replace("Used:","").replace("\n","").strip()
                remaining = usedAndRemaining[1].replace("Remaining:","").replace("\n","").strip()
                EligibilityPatientVerification.update({"IndividualAnnualDeductible":totals})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":remaining})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":used})
                EligibilityDeductiblesProcCode.append({
                    "Type": "Individual Annual Deductible",
                    "Network": "In Network",
                    "Amount": totals,
                    "Remaining": remaining,
                    "Used": used,
                    "ServiceCategory": "",
                    "BenefitPeriod": EligibilityPatientVerification.get("InsuranceCalendarOrFiscalPolicyYear"),
                    "Family_Individual": "Individual"
                })





    #Eligibility Benefits#
    for benefits in EligibilityBenefitsData:
        if "ERROR" in benefits.get("Description"):
            continue
        description = benefits.get("Description").split("-")[1].strip()+"---"+procCodeDesc.get(benefits.get("Proccode"))

        if benefits.get("Proccode") == "D2391":
            EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":benefits.get("WaitingPeriod")})
        
        EligibilityBenefits.append({
            "ProcedureCode": benefits.get("Proccode"),
            "ProcedureCodeDescription": description.replace("\u2013 ","").lower(),
            "Amount": "",
            "Type": benefits.get("BenefitClass"),
            "limitation": "Waiting Period: "+ benefits.get("WaitingPeriod"),
            "DeductibleApplies": benefits.get("DeductibleApplies"),
            "Copay": "",
            "Benefits": benefits.get("Copay"),
            "historyDates": ""
        })

    for treatment in EligibilityTreatmentHistory:
        defualtKeyword = treatment.get("Type")
        keyword = treatment.get("Type").lower()
        if "s" in keyword[-1:]:
            keyword = keyword[:-1]
        elif "es" in keyword[-2:]:
            keyword = keyword[:-2]

        if defualtKeyword == "Bitewing X-Rays":
            keyword = "Bitewing"
        if defualtKeyword == "Full Mouth/Panoramic X-Rays":
            keyword = "Panoramic radiographic image"
        if defualtKeyword == "Periodic Exams":
            keyword = "Periodic oral evaluation"
        if defualtKeyword == "Problem Focused Exams":
            keyword = "Limited oral evaluation - problem focused"

        keyword = keyword.lower()
        for benefitsSearch in EligibilityBenefits:
            if keyword in benefitsSearch.get("ProcedureCodeDescription"):
                #print(benefitsSearch.get("ProcedureCode"))
                benefitsSearch["limitation"] = treatment.get("HowManyAllowed")+", "+treatment.get("AgeLimit")+", "+benefitsSearch.get("limitation")
                benefitsSearch["historyDates"] = treatment.get("NextAvailable")

        
    for benefitsSort in EligibilityBenefits:
        if "---" in benefitsSort.get("ProcedureCodeDescription"):
            benefitsSort["ProcedureCodeDescription"] = benefitsSort.get("ProcedureCodeDescription").split("---")[0]

    
    for benefitsHistory in EligibilityBenefits:
        if benefitsHistory.get("historyDates") != "":
            EligibilityServiceTreatmentHistory.append({
                "ProcedureCode": benefitsHistory.get("ProcedureCode"),
                "LimitationText": benefitsHistory.get("limitation"),
                "History": benefitsHistory.get("historyDates"),
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": benefitsHistory.get("ProcedureCodeDescription")
            })
            TreatmentHistorySummary.append({
                "ProcedureCode": benefitsHistory.get("ProcedureCode"),
                "LimitationText": benefitsHistory.get("limitation"),
                "History": benefitsHistory.get("historyDates"),
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": benefitsHistory.get("ProcedureCodeDescription")
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

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\delta dental virginia\SD%20Payor%20Scraping\virginia.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\delta dental virginia\SD%20Payor%20Scraping\output_.json", 'r'))
# output=main(data, request)
# with open("deltadentalvirginiaPatient.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
