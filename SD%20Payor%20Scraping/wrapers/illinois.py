from mapPDF import mapEligibilityPatientVerification
from datetime import datetime
import json
from re import search
import re

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
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")[0]
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")
    EligibilityTreatmentHistory = Scraperdata.get("EligibilityServiceTreatmentHistory")
    EligibilityOtherProvisions = Scraperdata.get("EligibilityOtherProvisions")

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]

    if EligibilityPatient.get("InsuranceCalendarOrFiscalPolicyYear", None):
        beniftyear = EligibilityPatient.get("InsuranceCalendarOrFiscalPolicyYear").split(":")
        beniftyear = beniftyear[1].split(".")
        EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":beniftyear[0].strip()})

    EligibilityPatientVerification.update({"FamilyMemberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"SubscriberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"SubscriberName":EligibilityPatient.get("SubcriberName").replace("SUBSCRIBER NAME: ", "")})
    EligibilityPatientVerification.update({"ProgramType":EligibilityPatient.get("CoverageType").replace("COVERAGE TYPE: ", "")})
    EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":patientdata.get("BirthDate")})
    EligibilityPatientVerification.update({"SubscriberDateOfBirth":patientdata.get("SubscriberBirthDate")})
    EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("GroupName").replace("GROUP NAME: ", "")})
    EligibilityPatientVerification.update({"GroupNumber":EligibilityPatient.get("GroupNumber").replace("GROUP NUMBER: ", "")})
    EligibilityPatientVerification.update({"ClaimPayerID":EligibilityPatient.get("ElectronicPayerID").replace("ELECTRONIC CLAIMS PAYER ID: ", "")})
    EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":EligibilityPatient.get("ChildCoverageAge").replace("Child Coverage Age: ", "")})
    EligibilityPatientVerification.update({"DependentStudentAgeLimit":EligibilityPatient.get("StudentCoverageAge").replace("Student Coverage Age: ", "")})
    EligibilityPatientVerification.update({"OrthodonticAgeLimits":EligibilityPatient.get("DependentOrthodonticAge").replace("Dependent Orthodontic Age: ", "")})
    EligibilityPatientVerification.update({"AdultOrthodonticCovered":EligibilityPatient.get("AdultOrthodontic").replace("Adult Orthodontic: ", "")})
    EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})
    EligibilityPatientVerification.update({"CoordinationofBenefitsType":"Standard Coordination of Benefits"})
    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    EligibilityPatientVerification.update({"ClaimsAddress":EligibilityPatient.get("mailingAddress").replace("\n", " ")})
    EligibilityPatientVerification.update({"ClaimMailingAddress":EligibilityPatient.get("mailingAddress").replace("\n", " ")})



    familywaitingperiod = ""
    ###-----otherProvisions-----####
    WaitingPeriod = EligibilityOtherProvisions[1].get("WaitingPeriod")
    for item in WaitingPeriod:
        if item.get("Services1") == "PREVENTIVE":
            familywaitingperiod = item.get("Duration1")
            EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":familywaitingperiod})
        elif item.get("Services2") == "PREVENTIVE":
            familywaitingperiod = item.get("Duration2")
            EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":familywaitingperiod})
    
    
    FrequencyAgeAndBenefitLimitations = EligibilityOtherProvisions[0].get("FrequencyAgeAndBenefitLimitations")
    for item in FrequencyAgeAndBenefitLimitations:
        if search("Resin", item.get("Services")):
            EligibilityPatientVerification.update({"AlternativeBenefitProvision":item.get("Services")+" , "+item.get("FrequencyAndLimitation")})
        elif search("Missing Tooth Clause", item.get("Services")):
                    EligibilityPatientVerification.update({"MissingToothClause":item.get("FrequencyAndLimitation")})
        elif search("Predetermination", item.get("Services")):
                    EligibilityPatientVerification.update({"PreCertRequired":item.get("FrequencyAndLimitation")})
                    EligibilityPatientVerification.update({"PreauthorizationRequired":item.get("FrequencyAndLimitation")})
    ###-----otherProvisions-----####


    ####----Maximums and deductibles-----###
    MaximumsDeductiblestUsed = EligibilityMaximiums[0].get("MaximumsDeductiblesAmountUsed")

    individualannualdeductiblemet = ""
    individualannualbenefitusedtodate = ""
    ortholifetimebenefitusedtodate =""
    familyannualdeductiblemet = ""
    familyannuabenefitusedtodate = ""

    for item in MaximumsDeductiblestUsed[1:]:
        if item.get("Name") != "FAMILY DEDUCTIBLES & MAXIMUMS":
            Informaiton = str(item.get("Name")).split("Birthdate")
            name = Informaiton[0]
            Informaiton = Informaiton[1].split("Start")
            birthdate = Informaiton[0].strip()
            Informaiton = Informaiton[1].split("End")
            start = Informaiton[0].strip()
            end = Informaiton[1]

            if(str(patientdata.get("BirthDate")) == birthdate):
                EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
                EligibilityPatientVerification.update({"FamilyMemberName":name})
                EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":start})
                EligibilityPatientVerification.update({"FamilyMemberEndDate":end})

                individualannualdeductiblemet = item.get("RegANNDeductible")
                # print('individualannualdeductiblemet:-',individualannualdeductiblemet)
                individualannualbenefitusedtodate = item.get("RegANNMaximum")
                # print('individualannualbenefitusedtodate:-',individualannualbenefitusedtodate)
                ortholifetimebenefitusedtodate = item.get("OrthoLifeMaximum")
                # print('ortholifetimebenefitusedtodate:-',ortholifetimebenefitusedtodate)

                EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":individualannualdeductiblemet}) #
                EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":individualannualbenefitusedtodate}) #
                EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":ortholifetimebenefitusedtodate}) #
                


            if(str(patientdata.get("SubscriberBirthDate")) == birthdate):
                EligibilityPatientVerification.update({"SubscriberEffectiveDate":start})
                EligibilityPatientVerification.update({"SubscriberEndDate":end})
        
        elif item.get("Name") == "FAMILY DEDUCTIBLES & MAXIMUMS":
                familyannualdeductiblemet = item.get("RegANNDeductible")
                # print('familyannualdeductiblemet:-',familyannualdeductiblemet)
                familyannuabenefitusedtodate = item.get("RegANNMaximum")
                # print('familyannuabenefitusedtodate:-',familyannuabenefitusedtodate)

                EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":familyannualdeductiblemet}) #
                EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":familyannuabenefitusedtodate})

                
    MaximumsDeductiblesttotals = EligibilityMaximiums[1].get("MaximumsDeductiblesTotals")
    for item in MaximumsDeductiblesttotals:

        familyannualdeductible1 = ""
        ortholifetimebenefit = ""
        individualannualdeductible =""
        indiviannualmaxbenefit = ""

        if item.get("Maximum/Deductible") == "Annual Family Deductibles":
            familyannualdeductible1 = item.get("DeltaDentalPPO")
            # print('familyannualdeductible1:-',familyannualdeductible1)
            EligibilityPatientVerification.update({"FamilyAnnualDeductible":familyannualdeductible1})

        elif item.get("Maximum/Deductible") == "Ortho Lifetime Maximums":
            ortholifetimebenefit = item.get("DeltaDentalPPO")
            # print('ortholifetimebenefit:-',ortholifetimebenefit)
            EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":ortholifetimebenefit})

        elif item.get("Maximum/Deductible") == "Annual Deductibles":
            individualannualdeductible = item.get("DeltaDentalPPO")
            # print('individualannualdeductible:-',individualannualdeductible)
            EligibilityPatientVerification.update({"IndividualAnnualDeductible":individualannualdeductible})

        elif item.get("Maximum/Deductible") == "Annual Maximums":
            indiviannualmaxbenefit = item.get("DeltaDentalPPO")
            # print('indiviannualmaxbenefit:-',indiviannualmaxbenefit)
            EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":indiviannualmaxbenefit})
    try:        
        familyannualemaining  = calculate_difference(EligibilityPatientVerification.get("FamilyAnnualDeductible").strip(),EligibilityPatientVerification.get("FamilyAnnualDeductibleMet").strip())
        # print(familyannualemaining)
        EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":familyannualemaining})
    except:
        pass

    try:    
        indiannualremaining = calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleMet").strip())
        # print('indiannualremaining:- ',indiannualremaining)
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":indiannualremaining})
    except:
        pass

    try:
        indiannualremainingbenefit = calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualBenefitsUsedtoDate").strip())
        # print('indiannualremainingbenefit:-',indiannualremainingbenefit)
        EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":indiannualremainingbenefit})
    except:
        pass

    try:
        ortholifetimereminingbenefit = calculate_difference(EligibilityPatientVerification.get("OrthodonticLifetimeBenefit").strip(),EligibilityPatientVerification.get("OrthodonticLifetimeBenefitUsedtoDate").strip())
        # print('ortholifetimereminingbenefit:-',ortholifetimereminingbenefit)
            
        EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":ortholifetimereminingbenefit})
    except:
        pass

        
        
    


    ###----Maximiums-----###
                    
    EligibilityMaximums.append({
        "Type": "Annual Maximums",
        "Network": "PPO",
        "Amount": EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits"),
        "Remaining": EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit"),
        "ServiceCategory": "Dental",
        "Family_Individual": "Individual"
    })
    EligibilityMaximums.append({
        "Type": "Orthodontic Lifetime",
        "Network": "PPO",
        "Amount": EligibilityPatientVerification.get("OrthodonticLifetimeBenefit"),
        "Remaining": EligibilityPatientVerification.get("OrthodonticLifetimeRemainingBenefit"),
        "ServiceCategory": "Orthodontics",
        "Family_Individual": "Individual"
    })
    EligibilityDeductiblesProcCode.append({
        "Type": "Individual Annual Deductible",
        "Network": "PPO",
        "Amount": EligibilityPatientVerification.get("IndividualAnnualDeductible"),
        "Remaining": EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining"),
        "ServiceCategory": "Dental",
        "Family_Individual": "Individual"
    })
    EligibilityDeductiblesProcCode.append({
        "Type": "Orthodontic Lifetime",
        "Network": "PPO",
        "Amount": EligibilityPatientVerification.get("FamilyAnnualDeductible"),
        "Remaining": EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining"),
        "ServiceCategory": "Dental",
        "Family_Individual": "Family"
    })


    ##----benefits----##
    for item in EligibilityBenefitsData:
        desc = str(item.get("ProcedureName")).split("-", 1)
        deduct = "N/A"
        histroyDate = "N/A"
        benefit = "N/A"
        prodcedurecoddesc = ""
        limit = ""
        

        if item.get("DeltaDentalPPO") != "":
            benefit = item.get("DeltaDentalPPO")

        if item.get("Comments") is not None:
            if "Deductible does not apply." in item.get("Comments"):
                deduct = "No"
            elif "Deductible Applies." in item.get("Comments"):
                deduct = "Yes"

        descpt = desc[1].strip()
        matched_procedure = None
        matched_date = None

        for history in EligibilityTreatmentHistory:
            procedure_lists = [
                history.get("procedure1"),
                history.get("procedure2"),
                history.get("procedure3")
            ]
            for procedure in procedure_lists:
                if descpt in procedure or (re.search(r's-\d', descpt) and descpt.split('s-')[0] in procedure):
                    matched_procedure = procedure
                    matched_date = history.get("DateOfService" + str(procedure_lists.index(procedure) + 1))
                    break
            if matched_procedure:
                break

        if matched_procedure is not None:
            histroyDate = matched_date
            print('Matched Procedure:', matched_procedure)
            print('Matched Date:', histroyDate)    


        # for history in EligibilityTreatmentHistory:
        #     print(history.get("procedure1"))
        #     print(desc[1].strip())
        #     if search(history.get("procedure1").split(" ")[0], desc[1].strip()):
        #         histroyDate = history.get("DateOfService1")
        #     elif search(history.get("procedure2").split(" ")[0], desc[1].strip()):
        #         histroyDate = history.get("DateOfService2")
        #     elif search(history.get("procedure3").split(" ")[0], desc[1].strip()):
        #         histroyDate = history.get("DateOfService3")
                    

        if histroyDate == "":
            histroyDate = "N/A"    

        if len(desc) > 1:      
            prodcedurecoddesc = desc[1].strip()

        if item.get("Comments") is not None:
            limit = item.get("Comments").replace("Deductible does not apply.", "").replace("Deductible Applies.", "").strip()

        EligibilityBenefits.append({
            "ProcedureCode": "D"+item.get("Proccode"),
            "ProcedureCodeDescription": prodcedurecoddesc,
            "Amount": "",
            "Type": item.get("Type"),
            "limitation": limit,
            "DeductibleApplies": deduct,
            "Copay": "",
            "Benefits": benefit
        })

        EligibilityServiceTreatmentHistory.append({
            "ProcedureCode": "D"+item.get("Proccode"),
            "LimitationText": limit,
            "History": histroyDate,
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": prodcedurecoddesc
        })
        TreatmentHistorySummary.append({
            "ProcedureCode": "D"+item.get("Proccode"),
            "LimitationText": limit,
            "History": histroyDate,
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": prodcedurecoddesc
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

# request=json.load(open(r"C:\BPK\Eligibility_Python\VSCODE\10_05\SD Payor Scraping\smaple3.json", 'r'))
# data=json.load(open(r"C:\BPK\Eligibility_Python\VSCODE\10_05\SD Payor Scraping\output.json", 'r'))
# output=main(data, request)
# with open("illinoisWrapperOutput-Gabrielle.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
