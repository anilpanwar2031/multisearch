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
        if item.get("Group", None):
            EligibilityPatient  = item
        if item.get("BirthDate",None):
            if item.get("BirthDate") == patientdata.get("BirthDate"):
                EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
                EligibilityPatientVerification.update({"Relationship":item.get("Relationship")})
                EligibilityPatientVerification.update({"FamilyMemberName":item.get("Name")})
                EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":item.get("CoverageEffectiveDate")})
                EligibilityPatientVerification.update({"FamilyMemberEndDate":item.get("TermDate").replace("-","")})
        if item.get("Relationship") == "Subscriber":
            EligibilityPatientVerification.update({"SubscriberName":item.get("Name")})
            EligibilityPatientVerification.update({"SubscriberDateOfBirth":item.get("BirthDate")})
            EligibilityPatientVerification.update({"SubscriberEffectiveDate":item.get("CoverageEffectiveDate")})
            EligibilityPatientVerification.update({"SubscriberEndDate":item.get("TermDate").replace("-","")})
    


    EligibilityPatientVerification.update({"FamilyMemberId":patientdata.get("PatientMemberId")})
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"PlanType":EligibilityPatient.get("Coverage").replace("Coverage: ","")})
    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":EligibilityPatient.get("Coverage").replace("Coverage: ","")})
    EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":patientdata.get("BirthDate")})
    EligibilityPatientVerification.update({"InNetworkOutNetwork":"In Network"})
    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    #EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})
    EligibilityPatientVerification.update({"AdultOrthodonticCovered":EligibilityPatient.get("AdultOrthodontic").replace("Adult Orthodontic:","").strip().replace("N","No")})
    EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":EligibilityPatient.get("ChildCoverageAge").replace("Child Coverage Age:","").strip()})
    EligibilityPatientVerification.update({"DependentStudentAgeLimit":EligibilityPatient.get("StudentCoverageAge").replace("Student Coverage Age:","").strip()})
    EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":EligibilityPatient.get("WaitingPeriod")})
    EligibilityPatientVerification.update({"OrthodonticAgeLimits":EligibilityPatient.get("DependentOrthoAge").replace("Dependent Orthodontic Age: ","")})
    try:
        EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("Group").replace("Group:","").split("(")[0].strip()})
        EligibilityPatientVerification.update({"GroupNumber":EligibilityPatient.get("Group").replace("Group:","").split("(")[1].replace(")","").strip()})
    except:
         EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("Group").replace("Group:","").strip()})

    specialCondition = EligibilityPatient.get("SpecialCondtion")
    if "Group does not have missing tooth clause" in specialCondition:
        EligibilityPatientVerification.update({"MissingToothClause":"Group does not have missing tooth clause"})
    
    for pageItems in EligibilityDeductiblesProcCodeData:
        for name in pageItems:
            if "PosteriorComposite" in name:
                EligibilityPatientVerification.update({"AlternativeBenefitProvision":pageItems.get(name)})


    
    EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":EligibilityPatient.get("CalenderYear").replace("Program deductibles and maximums are calculated for a \"Benefit Year\" defined as","").replace("Subscribers are responsible for paying the following deductible before Delta Dental will make payment.","").replace(".","").strip()})
    # EligibilityPatientVerification.update({"MissingToothClause":EligibilityPatient.get("MissingToothClause")})
    # EligibilityPatientVerification.update({"CoordinationofBenefitsType":EligibilityPatient.get("CoordinaitonOfBenefit")})
    EligibilityPatientVerification.update({"ClaimPayerID":"CDIA1"})
    EligibilityPatientVerification.update({"ClaimMailingAddress":"DELTA DENTAL OF IOWA, P.O. BOX 9000, JOHNSTON, IA 50131"})
    EligibilityPatientVerification.update({"ClaimsAddress":"DELTA DENTAL OF IOWA, P.O. BOX 9000, JOHNSTON, IA 50131"})

    

    # ####----Maximums and deductibles-----###
    for itemMax in EligibilityMaximiums:
        if itemMax.get("Type") == "Annual Family Maximums":   
            EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":itemMax.get("DeltaDentalPpo")})
            #EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":itemMax.get("FamilyUsed")})
            #EligibilityPatientVerification.update({"FamilyAnnualRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("FamilyAnnualBenefitsUsedtoDate").strip())})
            EligibilityMaximums.append({
                "Type": "Maximum",
                "Network": "In Network",
                "Amount": itemMax.get("DeltaDentalPpo"),
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Family"
            })

        if itemMax.get("Type") == "Annual Maximums":
            EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":itemMax.get("DeltaDentalPpo")})
            #EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":itemMax.get("IndividualsUsed")})
            #EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate").strip())})
            EligibilityMaximums.append({
                "Type": "Maximum",
                "Network": "In Network",
                "Amount": itemMax.get("DeltaDentalPpo"),
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })

        if itemMax.get("Type") == "Individual Annual Deductible":
            EligibilityPatientVerification.update({"IndividualAnnualDeductible":itemMax.get("DeltaDentalPpo")})
            #EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":itemMax.get("IndividualsUsed")})
            #EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleMet").strip())})
            EligibilityDeductiblesProcCode.append({
                "Type": "Deductible",
                "Network": "In Network",
                "Amount": itemMax.get("DeltaDentalPpo"),
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Individual"
            })

        if itemMax.get("Type") == "Family Annual Deductible":
            EligibilityPatientVerification.update({"FamilyAnnualDeductible":itemMax.get("DeltaDentalPpo")})
            #EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":itemMax.get("FamilyUsed")})
            #EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualDeductible").strip(),EligibilityPatientVerification.get("FamilyAnnualDeductibleMet").strip())})
            EligibilityDeductiblesProcCode.append({
                "Type": "Deductible",
                "Network": "In Network",
                "Amount": itemMax.get("DeltaDentalPpo"),
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "",
                "BenefitPeriod": "",
                "Family_Individual": "Family"
            })

        if itemMax.get("Type") == "Ortho Lifetime Maximum":
            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":itemMax.get("DeltaDentalPpo")})
            #EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":itemMax.get("IndividualsUsed")})
            #EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate").strip())})
            EligibilityMaximums.append({
                "Type": "Ortho Lifetime Maximum",
                "Network": "In Network",
                "Amount": itemMax.get("DeltaDentalPpo"),
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "Orthodontic",
                "BenefitPeriod": "",
                "Family_Individual": ""
            })

        if itemMax.get("Type") == "Ortho Annual Deductibles":
            #EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":itemMax.get("DeltaDentalPpo")})
            #EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":itemMax.get("IndividualsUsed")})
            #EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate").strip())})
            EligibilityMaximums.append({
                "Type": "Ortho Annual Deductibles",
                "Network": "In Network",
                "Amount": itemMax.get("DeltaDentalPpo"),
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "Orthodontic",
                "BenefitPeriod": "",
                "Family_Individual": ""
            })

        if itemMax.get("Type") == "Ortho Lifetime Deductibles":
            #EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":itemMax.get("DeltaDentalPpo")})
            #EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":itemMax.get("IndividualsUsed")})
            #EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeBenefitsUsedtoDate").strip())})
            EligibilityMaximums.append({
                "Type": "Ortho Lifetime Deductibles",
                "Network": "In Network",
                "Amount": itemMax.get("DeltaDentalPpo"),
                "Remaining": "",
                "Used": "",
                "ServiceCategory": "Orthodontic",
                "BenefitPeriod": "",
                "Family_Individual": ""
            })

    
    for benefits in EligibilityBenefitsData:
        description = ""
        codeN = "coodeistobefetched"
        if "[" in benefits.get("code"):
            description = benefits.get("code").split("[")[1].replace("]","")
            codeN = "D"+benefits.get("code").split("[")[0].strip()
        else:
            description = benefits.get("code")

        
        descriptionStrip = description
        descriptionStrip = descriptionStrip.replace(" ","")
        limitationsText = ""
        frequency = ""
        for page in EligibilityDeductiblesProcCodeData:
            for limitations in page:
                if search(descriptionStrip,limitations):
                    limitationsText = page.get(limitations)
                    if(descriptionStrip == "Exams" and "Consultations" in limitations):
                        limitationsText = ""
                elif description == "Posterior Composites":
                    if search("PosteriorComposite",limitations):
                        limitationsText = page.get(limitations)
                elif description == "Stainless Crowns":
                    if search("StainlessSteelCrowns",limitations):
                        limitationsText = page.get(limitations)
                elif description == "Simple Oral Surgery":
                    if search("OralSurgery",limitations):
                        limitationsText = page.get(limitations)
                elif description == "Occlusal X-Rays":
                    if search("OcclusalXRays",limitations):
                        limitationsText = page.get(limitations)
                elif description == "Bitewing X-Rays":
                    if search("BitewingXRays",limitations):
                        limitationsText = page.get(limitations)
                elif description == "Peripical X-Rays":
                    if search("PaXRays",limitations):
                        limitationsText = page.get(limitations)

                limitations1 = limitations
                try:
                    sperateLimitaion = limitations1.replace("Code",",").replace("Codes",",").replace("And",",").split(",")
                    limitationsNew = ""
                    for itemSperateLimitaion in sperateLimitaion:
                        limitationsNew = limitationsNew+ "D"+itemSperateLimitaion

                    if codeN in limitationsNew:
                        limitationsText = page.get(limitations)
                except:
                    pass

        for elems in TreatmentHistorySummaryData:
            if description in elems.get("Benefit"):
                frequency = elems.get("FreqLimitPP0").replace("See B below","")


        EligibilityBenefits.append({
            "ProcedureCode": benefits.get("Proccode"),
            "ProcedureCodeDescription": description,
            "Amount": "",
            "Type": "",
            "limitation": str(frequency+", "+limitationsText+ ", Age limit "+benefits.get("AgeLimitPPO")).strip(", ").replace(", ,",","),
            "DeductibleApplies": benefits.get("DeductiblePPO"),
            "Copay": "",
            "Benefits": benefits.get("benefitPPO")
        })
        


    for hist in EligibilityBenefits:
        code = hist.get("ProcedureCode").replace("D","").lstrip("0")

        historyDates = ""
        tooth = ""
        surface = ""
        for dates in EligibilityTreatmentHistory:
            if code == dates.get("ProcCode"):
                # if dates.get("Tooth") == "NA" and dates.get("ToothSurface") == "NA":
                #     dateToothSurface = dates.get("DateOfService")
                # else:
                dateToothSurface = str(dates.get("DateOfService"))+"-"+str(dates.get("Tooth"))+"-"+str(dates.get("ToothSurface"))
                if dateToothSurface in historyDates:
                    continue
                historyDates = historyDates + dateToothSurface+", "
                tooth = tooth + dates.get("Tooth")+", "
                surface = surface + dates.get("ToothSurface")+", "
        
        EligibilityServiceTreatmentHistory.append({
            "ProcedureCode": hist.get("ProcedureCode"),
            "LimitationText": hist.get("limitation"),
            "History": historyDates.strip(", ").replace("-NA-NA",""),
            "Tooth": tooth.strip(", "),
            "Surface": surface.strip(", "),
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": hist.get("ProcedureCodeDescription")
        })
        TreatmentHistorySummary.append({
            "ProcedureCode": hist.get("ProcedureCode"),
            "LimitationText": hist.get("limitation"),
            "History": historyDates.strip(", ").replace("-NA-NA",""),
            "Tooth": tooth.strip(", "),
            "Surface": surface.strip(", "),
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": hist.get("ProcedureCodeDescription")
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

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\iowa DD\30 july\SD%20Payor%20Scraping\iowa2.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\iowa DD\30 july\SD%20Payor%20Scraping\output_42097.json", 'r'))
# output=main(data, request)
# with open("IowaOutput-Garner-Paglisotti.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
