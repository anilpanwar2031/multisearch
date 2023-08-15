from mapPDF import mapEligibilityPatientVerification
from datetime import datetime
import json

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
    return f'${float(a)-float(b)}'
def getsum(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    return f'${float(a)+float(b)}'
def main(data, request):
    
    patientdata = request.get("PatientData")[0]
    EligibilityPatientData = data.get("EligibilityPatientVerification")[0]
    EligibilityOtherProvisionsData = data.get("EligibilityOtherProvisions")
    EligibilityPatientVerification=mapEligibilityPatientVerification()
    
    
    planTypeText = ""
    if ":" in EligibilityPatientData.get("Plan"):
        planTypeText = EligibilityPatientData.get("Plan").split(":")[0].strip()
    else:
        planTypeText = EligibilityPatientData.get("Plan").strip()

    

    patientEffectiveDate = ""
    patientEndDate = ""
    for dateItems in EligibilityOtherProvisionsData:
        date_str = dateItems.get("TerminationDate")
        date_format = "%m/%d/%Y"
        target_date = datetime.strptime(date_str, date_format).date()
        current_date = datetime.now().date()
        if (dateItems.get("PlanDescription") in planTypeText and target_date > current_date):
            EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
            patientEffectiveDate = dateItems.get("EffectiveDate")
            patientEndDate = dateItems.get("TerminationDate")



    
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate")})
    EligibilityPatientVerification.update({"SubscriberName":patientdata.get("SubscriberFirstName")+" "+patientdata.get("SubscriberLastName")})
    EligibilityPatientVerification.update({"FamilyMemberName":patientdata.get("FirstName")+" "+patientdata.get("LastName")})
    EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":patientdata.get("BirthDate")})
    
    
    
    EligibilityPatientVerification.update({"AlternativeBenefitProvision":"N/A"})
    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":"N/A"})
    EligibilityPatientVerification.update({"oonBenefits":"N/A"})
    EligibilityPatientVerification.update({"IndividualAnnualDeductible":"N/A"})
    EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":"N/A"})
    EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":"N/A"})
    EligibilityPatientVerification.update({"FamilyAnnualDeductible":"N/A"})
    EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":"N/A"})
    EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":"N/A"})
    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":"N/A"})
    EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":"N/A"})
    EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":"N/A"})
    EligibilityPatientVerification.update({"CoordinationofBenefits":"N/A"})
    EligibilityPatientVerification.update({"CoordinationofBenefitsType":"N/A"})
    EligibilityPatientVerification.update({"GroupName":"N/A"})
    EligibilityPatientVerification.update({"GroupNumber":"N/A"})
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    temp=data.get("EligibilityPatientVerification")[0]
    EligibilityPatientVerification.update({"FamilyMemberId":temp.get("Member ID").replace("Member ID: ", "")})
    EligibilityPatientVerification.update({"GroupNumber":temp.get("Insurance Group Number")})
    EligibilityPatientVerification.update({"FamilyMemberEndDate":patientEndDate})


    #elif target_date <= current_date:
        #EligibilityPatientVerification.update({"SubscriberEligibilityStatus":"Inactive"})

    EligibilityPatientVerification.update({"PlanType":planTypeText})
    EligibilityPatientVerification.update({"GroupName":planTypeText})
    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":temp.get("Insurance Calendar or Fiscal Policy Year").replace("Calendar Year Max: ", "")})
    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":planTypeText})
    EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":patientEffectiveDate})
    EligibilityPatientVerification.update({"ClaimMailingAddress":"GEHA PO Box 21542 Eagan, MN 55121"})
    EligibilityPatientVerification.update({"ClaimsAddress":"GEHA PO Box 21542 Eagan, MN 55121"})
    if(temp.get("Coverage")=="Coverage: Family"):
        EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":temp.get("Insurance Calendar or Fiscal Policy Year").replace("Calendar Year Max: ", "")})
    if("High Option" in temp.get("Plan")):
        EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    else:
        EligibilityPatientVerification.update({"oonBenefits":"No"})
    EligibilityPatientVerification.update({"AlternativeBenefitProvision":"We will limit benefits payable to the benefit that would have been payable if the least costly covered service had been provided. This is called alternate benefit."})
    
    standardoption={
        "Basic":{
            "InNetwork":"0%",
            "OutOfnetwork":"25%",
            "Description":"Class A. Covers two exams, two cleanings, and two sets of bitewing X-rays per calendar year"
            },
        "Teledentistry":{
            "InNetwork":"0%",
            "OutOfnetwork":"100%",
            "Description":"Class A. One oral evaluation per patient in a 12-consecutive-month period"
            },
        "Intermediate":{
            "InNetwork":"45%",
            "OutOfnetwork":"50%",
            "Description":"Class B. Covers restorations, extractions and periodontal maintenance"
            },
        "Major":{
            "InNetwork":"65%",
            "OutOfnetwork":"70%",
            "Description":"Class C. Covers root canals, crowns, bridges, dentures and periodontal surgery"
            },
        "Orthodontic":{
            "InNetwork":"50%",
            "InNetworkLifetimeMaximum":"$2,500",
            "OutOfnetwork":"50%",
            "OutOfnetworkLifetimeMaximum":"$1,500",
            "Description":"Class D. Covers adults and children orthodontic. No waiting periods."
            },
        "Calendar year maximum":{
            "InNetwork":"$2,500 per person",
            "OutOfnetwork":"$2,000 per person",
            "Description":"Class A, B and C services only"
        }
    }

    highoption={
        "Basic":{
            "InNetwork":"0%",
            "OutOfnetwork":"0%",
            "Description":"Class A. Covers two exams, two cleanings, and two sets of bitewing X-rays per calendar year"
            },
        "Teledentistry":{
            "InNetwork":"0%",
            "OutOfnetwork":"0%",
            "Description":"Class A. One oral evaluation per patient in a 12-consecutive-month period"
            },
        "Intermediate":{
            "InNetwork":"20%",
            "OutOfnetwork":"20%",
            "Description":"Class B. Covers restorations, extractions and periodontal maintenance"
            },
        "Major":{
            "InNetwork":"50%",
            "OutOfnetwork":"50%",
            "Description":"Class C. Covers root canals, crowns, bridges, dentures and periodontal surgery"
            },
        "Orthodontic":{
            "InNetwork":"30%",
            "InNetworkLifetimeMaximum":"$3,500",
            "OutOfnetwork":"30%",
            "OutOfnetworkLifetimeMaximum":"$3,500",
            "Description":"Class D. Covers adults and children orthodontic. No waiting periods."
            },
        "Calendar year maximum":{
            "InNetwork":"Unlimited per person",
            "OutOfnetwork":"Unlimited per person",
            "Description":"Class A, B and C services only"
        }
    }

    if("High Option" in temp.get("Plan")):
        plan=highoption
        limitation0110="Three per calendar year"
        limitationClassA = "0%"
        
        limitationClassB = "20%"
        limitationClassC = "50%"
        limitationClassD = "30%"
        deductibleapplies="No"
        limitation1110="Thrice per calendar year"
    else:
        plan=standardoption
        # EligibilityPatientVerification.update({"FamilyAnnualDeductible":"$75"})
        # EligibilityPatientVerification.update({"IndividualAnnualDeductible":"$25"})
        limitation0110="Twice per calendar year"
        limitationClassA = "0%"
        limitationClassB = "45%"
        limitationClassC = "65%"
        limitationClassD = "50%"
        deductibleapplies="No"
        limitation1110="Thrice per calendar year"
    EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":plan.get("Calendar year maximum").get("InNetwork").replace(" per person", "")})
    
    EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":plan.get("Orthodontic").get("InNetworkLifetimeMaximum").replace(" per person", "")})
    EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":plan.get("Orthodontic").get("InNetworkLifetimeMaximum").replace(" per person", "")})
    EligibilityPatientVerification.update({"OrthodonticAgeLimits":"Unmarried dependent children under age 22"})
    EligibilityPatientVerification.update({"AdultOrthodonticCovered":"Yes"})
    EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})
    EligibilityPatientVerification.update({"CoordinationofBenefitsType":"As with all FEDVIP plans, dental benefits available from your FEHB carrier will be considered before we calculate benefits paid by GEHA."})
    EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":"Unmarried dependent children under age 22"})
    EligibilityPatientVerification.update({"DependentStudentAgeLimit":"23"})
    EligibilityPatientVerification.update({"TreatmentinProgressCoverage":"In-progress treatment for dependents of retiring TDP enrollees will be covered for the 2023 plan year"})
    EligibilityPatientVerification.update({"PreauthorizationRequired":"To obtain a pre-determination, the dentist should submit a completed dental pre-treatment estimate claim form that itemizes the proposed procedure codes, charge for each procedure along with pre-treatment plan, radiographic images and any other diagnostic materials."})
    # "To obtain a pre-determination, the dentist should submit a completed dental pre-treatment estimate claim form that itemizes the proposed procedure codes, charge for each procedure along with pre-treatment plan, radiographic images and any other diagnostic materials."
    EligibilityPatientVerification.update({"MedicallyNecessaryonly":"Yes"})
    HowAreBenefitsPaid="The total case fee and the maximum allowed amount will be divided by the number of months for the total treatment plan. Each resulting portion will be considered to be incurred on a quarterly basis until the lifetime maximum is paid, treatment is completed or eligibility ends, whichever comes first."
    limitation="D0140 Limited oral evaluation - problem focused - One limited oral evaluation, problem-focused (D0140) will be allowed per patient per dentist in a 12 consecutive month period. A limited oral evaluation will be considered integral when provided on the same date of service by the same dentist as any other oral evaluation"
    EligibilityPatientVerification.update({"HowAreBenefitsPaid":HowAreBenefitsPaid})
    EligibilityBenefits=[
        {

            "ProcedureCode": "D0120",
            "ProcedureCodeDescription": "Periodic oral evaluation",
            "limitation": "Two times per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {
            "ProcedureCode": "D0140",
            "ProcedureCodeDescription": "Limited oral evaluation",
            "limitation": "One limited oral evaluation will be allowed per patient per dentist in a 12 consecutive month period.",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {
            "ProcedureCode": "D0145",
            "ProcedureCodeDescription": "Oral evaluation for a patient under three years of age and counseling with primary caregiver",
            "limitation": "Two times per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {
            "ProcedureCode": "D0150",
            "ProcedureCodeDescription": "Comprehensive oral evaluation",
            "limitation": "Two times per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {
            "ProcedureCode": "D0170",
            "ProcedureCodeDescription": "N/A",
            "limitation": "N/A",
            "DeductibleApplies": "N/A",
            "Copay": "N/A",
            "Benefits": "N/A"
        },
        {
            "ProcedureCode": "D0180",
            "ProcedureCodeDescription": "Comprehensive periodontal evaluation",
            "limitation": "Two times per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0210",
            "ProcedureCodeDescription": "Intraoral - comprehensive series of radiographic images",
            "limitation": "Once every 3 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0220",
            "ProcedureCodeDescription": "Intraoral - periapical first radiographic image",
            "limitation": "",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0230",
            "ProcedureCodeDescription": "Intraoral - periapical - each additional radiographic image",
            "limitation": "",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0240",
            "ProcedureCodeDescription": "Intraoral - occlusal radiographic image",
            "limitation": "4 per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0250",
            "ProcedureCodeDescription": "Extra-oral - 2D projection radiographic image creating using a stationary radiation source, and detector",
            "limitation": "4 per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0251",
            "ProcedureCodeDescription": "Extra-oral - posterior dental radiographic image",
            "limitation": "4 per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0270",
            "ProcedureCodeDescription": "Bitewing - single radiographic image",
            "limitation": "Twice per Calendar Year for children 22 and younger and once per Calendar Year for adults 23 and older",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0272",
            "ProcedureCodeDescription": "Bitewings - two radiographic image",
            "limitation": "Twice per Calendar Year for children 22 and younger and once per Calendar Year for adults 23 and older",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0273",
            "ProcedureCodeDescription": "Bitewings - three radiographic image",
            "limitation": "Twice per Calendar Year for children 22 and younger and once per Calendar Year for adults 23 and older",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0274",
            "ProcedureCodeDescription": "Bitewings - four radiographic image",
            "limitation": "Twice per Calendar Year for children 22 and younger and once per Calendar Year for adults 23 and older",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0277",
            "ProcedureCodeDescription": "Vertical bitewings - 7 to 8 radiographic image",
            "limitation": "Twice per Calendar Year for children 22 and younger and once per Calendar Year for adults 23 and older",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0330",
            "ProcedureCodeDescription": "Panoramic radiographic image",
            "limitation": "Once every 3 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D0425",
            "ProcedureCodeDescription": "Caries susceptibility tests",
            "limitation": "",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1110",
            "ProcedureCodeDescription": "Prophylaxis - adult",
            "limitation": limitation1110,
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1120",
            "ProcedureCodeDescription": "Prophylaxis - child",
            "limitation": "Twice per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1206",
            "ProcedureCodeDescription": "Topical application of fluoride varnish",
            "limitation": "Limited to Covered Persons under age 22 twice per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1208",
            "ProcedureCodeDescription": "Topical application of fluoride - excluding varnish",
            "limitation": "Limited to Covered Persons under age 22 twice per Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1351",
            "ProcedureCodeDescription": "Sealant - per tooth",
            "limitation": "Limited to Covered Persons under 18 years of age on unrestored permanent molars only and are limited to one sealant per tooth every 3 Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1352",
            "ProcedureCodeDescription": "Preventive resin restoration in a moderate to high caries risk patient - permanent tooth",
            "limitation": "Limited to Covered Persons under 18 years of age on unrestored permanent molars only and are limited to one sealant per tooth every 3 Calendar Year",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1353",
            "ProcedureCodeDescription": "Sealant Repair - per tooth",
            "limitation": "Once per tooth, per lifetime",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1354",
            "ProcedureCodeDescription": "Application of caries arresting medicament - per tooth - per lifetime",
            "limitation": "Limited to children under 9 years of age",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1510",
            "ProcedureCodeDescription": "Space maintainer - fixed, unilateral - per quadrant",
            "limitation": "Limited to initial appliance, no more than one per tooth for non-orthodontic treatment of prematurely lost teeth in children under age 19",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1516",
            "ProcedureCodeDescription": "Space maintainer - fixed - bilateral, maxillary",
            "limitation": "Limited to initial appliance, no more than one per tooth for non-orthodontic treatment of prematurely lost teeth in children under age 19",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1517",
            "ProcedureCodeDescription": "Space maintainer - fixed - bilateral, mandibular",
            "limitation": "Limited to initial appliance, no more than one per tooth for non-orthodontic treatment of prematurely lost teeth in children under age 19",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1520",
            "ProcedureCodeDescription": "Space maintainer - removable, unilateral - per quadrant",
            "limitation": "Limited to initial appliance, no more than one per tooth for non-orthodontic treatment of prematurely lost teeth in children under age 19",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1526",
            "ProcedureCodeDescription": "Space maintainer - removable - bilateral, maxillary",
            "limitation": "Limited to initial appliance, no more than one per tooth for non-orthodontic treatment of prematurely lost teeth in children under age 19",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1527",
            "ProcedureCodeDescription": "Space maintainer - removable - bilateral, mandibular",
            "limitation": "Limited to initial appliance, no more than one per tooth for non-orthodontic treatment of prematurely lost teeth in children under age 19",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1575",
            "ProcedureCodeDescription": "Distal Shoe Space Maintainer - Fixed, Unilateral - per quadrant",
            "limitation": "Limited to initial appliance, no more than one per tooth for non-orthodontic treatment of prematurely lost teeth in children under age 19",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1551",
            "ProcedureCodeDescription": "Re-cement or re-bond bilateral space maintainer maxillary",
            "limitation": "Twice per Calendar Year combined with D1552 & D1553",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1552",
            "ProcedureCodeDescription": "Re-cement or rebond bilateral space maintainer - mandibular",
            "limitation": "Twice per Calendar Year combined with D1551 & D1553",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1553",
            "ProcedureCodeDescription": "Re-cement or re-bond unilateral space maintainer - per quadrant",
            "limitation": "Twice per Calendar Year combined with D1551 & D1552",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D1321",
            "ProcedureCodeDescription": "Counseling for the control and prevention of adverse oral, behavioral, and systemic health effects associated with high-risk substance use",
            "limitation": "Once per lifetime",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D2140",
            "ProcedureCodeDescription": "Amalgam one surface, primary or permanent",
            "limitation": "o one restoration per tooth surface every 2 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D2150",
            "ProcedureCodeDescription": "Amalgam two surfaces, primary or permanent",
            "limitation": "one restoration per tooth surface every 2 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D2160",
            "ProcedureCodeDescription": "Amalgam three surfaces, primary or permanent",
            "limitation": "one restoration per tooth surface every 2 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D2161",
            "ProcedureCodeDescription": "Amalgam four or more surfaces, primary or permanent",
            "limitation": "one restoration per tooth surface every 2 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D2391",
            "ProcedureCodeDescription": "Resin-based composite one surface, posterio",
            "limitation": "one restoration per tooth surface every 2 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D2392",
            "ProcedureCodeDescription": "Resin-based composite two surface, posterio",
            "limitation": "one restoration per tooth surface every 2 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D2393",
            "ProcedureCodeDescription": "Resin-based composite three surface, posterio",
            "limitation": "one restoration per tooth surface every 2 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D2394",
            "ProcedureCodeDescription": "Resin-based composite four or more surface, posterio",
            "limitation": "one restoration per tooth surface every 2 Calendar Years",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
                {

            "ProcedureCode": "D2930",
            "ProcedureCodeDescription": "Prefabricated stainless steel crown primary tooth",
            "limitation": "Limited to one per patient, per tooth, per lifetime for Covered Persons under 15 years of age",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D2933",
            "ProcedureCodeDescription": "N/A",
            "limitation": "N/A",
            "DeductibleApplies": "N/A",
            "Copay": "N/A",
            "Benefits": "N/A"
        },
        {

            "ProcedureCode": "D2934",
            "ProcedureCodeDescription": "N/A",
            "limitation": "N/A",
            "DeductibleApplies": "N/A",
            "Copay": "N/A",
            "Benefits": "N/A"
        },
        {

            "ProcedureCode": "D3220",
            "ProcedureCodeDescription": "Therapeutic pulpotomy (excluding final restoration)",
            "limitation": "Therapeutic pulpotomy is limited to once per tooth per lifetime",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D3230",
            "ProcedureCodeDescription": "Pulpal therapy (resorbable filling)",
            "limitation": "Limited to primary incisor teeth for children up to age 6 and cuspids up to age 11 and is limited to once per tooth per lifetime",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D3233",
            "ProcedureCodeDescription": "N/A",
            "limitation": "N/A",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D3234",
            "ProcedureCodeDescription": "N/A",
            "limitation": "N/A",
            "DeductibleApplies": "N/A",
            "Copay": "N/A",
            "Benefits": "N/A"
        },
        {

            "ProcedureCode": "D7140",
            "ProcedureCodeDescription": "Extraction, erupted tooth or exposed root (elevation and/or forceps removal)",
            "limitation": "N/A",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassB
        },
        {

            "ProcedureCode": "D9110",
            "ProcedureCodeDescription": "Palliative treatment of dental pain",
            "limitation": "Per visit",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D9230",
            "ProcedureCodeDescription": "Inhalation of nitrous oxide/analgesia, anxiolysis",
            "limitation": "limited to children under age 9 when performed with covered extractions and restorations",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassC
        },
        {

            "ProcedureCode": "D9310",
            "ProcedureCodeDescription": "Consultation (diagnostic service provided by dentist or physician other than requesting dentist orphysician)",
            "limitation": "Once per patient, per provider (dentist) per lifetime",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D9311",
            "ProcedureCodeDescription": "Consultation with a medical health care professional",
            "limitation": "Once per Covered Person per lifetime",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        },
        {

            "ProcedureCode": "D9440",
            "ProcedureCodeDescription": "Office visit after regularly scheduled hours",
            "limitation": "",
            "DeductibleApplies": deductibleapplies,
            "Copay": "",
            "Benefits": limitationClassA
        }        
    ]
    

    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Geha\bug 14 july\SD%20Payor%20Scraping\geha.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\Geha\bug 14 july\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data, request)
# with open("Gehares.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
