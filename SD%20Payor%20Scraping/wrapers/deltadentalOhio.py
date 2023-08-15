import json
from mapPDF import mapEligibilityPatientVerification
procCodeDesc=json.load(open("wrapers/procCodeDesc.json", 'r'))
def getclientbenefitinfo(text):
    temp={}
    for x in text.split('\n'):
        if(len(x.split(':'))==2):
            temp.update({x.split(':')[0].strip():x.split(':')[1].strip()})
    return temp
def mapdicts(a,b):
    for x in a:
        b.update({x:""})
    return b
def changeNone(val):
    if(val==None or val=="N/A"):
        return ""
    else:
        return val
def calculate_difference(a,b):
    if(a=="" or a==None):
        a="0.0"
    if(b=="" or b==None):
        b="0.0"
    a=a.replace(",", "").replace("N/A", "0").replace("$", "")
    b=b.replace(",", "").replace("N/A", "0").replace("$", "")
    return f'${float(a)-float(b)}'
def main(data, req=None):
    PatientData=req.get("PatientData")[0]
    EligibilityBenefitsData = data.get("EligibilityBenefits")
    EligibilityDeductiblesProcCodeData = data.get("EligibilityDeductiblesProcCode")
    EligibilityTreatmentHistory = data.get("EligibilityServiceTreatmentHistory")

    EligibilityPatientVerification={}
    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]

    state="Michigan"
    EligibilityPatientVerification.update({"ClaimMailingAddress":data.get("EligibilityOtherProvisions")[1].get("DeltaDentalofMichiganClaimMailingAddressGroupDentalBenefits").replace("\n", " ")})
    
    
    EligibilityPatientVerification.update({"InsuranceCalendarOrFiscalPolicyYear":data.get("EligibilityPatientVerification")[1].get("CalenderYear").replace("Accum Period Type:","").strip()})
    ClientPlanData=getclientbenefitinfo(data.get("EligibilityPatientVerification")[1].get("ClientBenefitInformation"))
    CobInformation=getclientbenefitinfo(data.get("EligibilityPatientVerification")[1].get("CobInformation"))
    if(CobInformation.get("Payment Option Type")):
        EligibilityPatientVerification.update({"CoordinationofBenefitsType":CobInformation.get("Payment Option Type")})
        EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})

    EligibilityPatientVerification.update({"InsuranceName":ClientPlanData.get("Plan")})
    # EligibilityPatientVerification.update({"PayerId":ClientPlanData.get("Payor ID")})
    EligibilityPatientVerification.update({"ClaimPayerID":ClientPlanData.get("Payor ID")})
    EligibilityPatientVerification.update({"GroupNumber":ClientPlanData.get("Group Number")})
    EligibilityPatientVerification.update({"GroupName":ClientPlanData.get("Group Name")})
    EligibilityPatientVerification.update({"PlanName":ClientPlanData.get("Product")})
    EligibilityPatientVerification.update({"PlanType":ClientPlanData.get("Plan")})
    PatientName=PatientData.get("FirstName").upper()+' '+PatientData.get("LastName").upper()
    EligibilityPatientVerification.update({"SubscriberId":PatientData.get("SubscriberId")})
    EligibilityPatientVerification.update({"FamilyMemberName":PatientName})
    EligibilityPatientVerification.update({"AlternativeBenefitProvision":"Yes"})

    try:
        if (data.get("EligibilityPatientVerification")[1].get("outofNetworkBenefit") != ""):
            EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    except:
        pass
    for x in data.get("EligibilityPatientVerification")[0].get("FamilyMembers"):
        if(x.get("Relationship")=="Subscriber"):
            EligibilityPatientVerification.update({("SubscriberName"):x.get("PatientName")})
            EligibilityPatientVerification.update({"SubscriberEffectiveDate":x.get("EffectiveDate")})
            EligibilityPatientVerification.update({"SubscriberDateOfBirth":x.get("Birthdate")})
            EligibilityPatientVerification.update({"SubscriberEligibilityStatus":x.get("Eligibility")})
        if(PatientData.get("BirthDate")==x.get("Birthdate") and x.get("Eligibility") == "Active"):
            EligibilityPatientVerification.update({"EligibilityStatus":x.get("Eligibility")})
            EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":x.get("EffectiveDate")})
            EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":x.get("Birthdate")})
    
    EligibilityMaximums, EligibilityDeductiblesProcCode=[], []
    for x in data.get("EligibilityMaximums"):
        temp={}
        tempmapdict={
                "Type": "",
                "ProgramDeductible_AppliesToTheFollowingServices_": "",
                "Network": "",
                "Amount": "",
                "Remaining": ""
            }
        temp=mapdicts(tempmapdict, temp)
        temp.update({"Type":x.get("Type")})
        temp.update({"Category":x.get("Category")})
        temp.update({"Name":x.get("Name")})
        temp.update({"CategoryHistoryAccumator":x.get("CategoryHistoryAccumator")})
        temp.update({"AccumPeriodFrom":x.get("AccumPeriodFrom")})
        
        for y in x.get("Individual").replace("\u00a0", ":").split():
            temp.update({f'Individual {y[:y.index(":")]}':y[y.index(":")+1:]})
        for y in x.get("Family").replace("\u00a0", ":").split():
            temp.update({f'Family {y[:y.index(":")]}':y[y.index(":")+1:]})
        if(x.get("Type")=="Maximum"):
            if(x.get("Category")=="General"): 
                EligibilityMaximums.append(temp)
                EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":temp.get("Individual Amount")})
                EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":temp.get("Individual Used")})
                EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":temp.get("Individual Remaining")})
                EligibilityPatientVerification.update({"FamilyAnnualMaximumBenefits":temp.get("Family Amount")})
                EligibilityPatientVerification.update({"FamilyAnnualBenefitsUsedtoDate":temp.get("Family Used")})
                EligibilityPatientVerification.update({"FamilyAnnualRemainingBenefit":temp.get("Family Remaining")})
                # EligibilityPatientVerification.update({"IndividualAnnualDeductible":temp.get("Individual Amount")})
            elif(x.get("Category")=="Orthodontic"):
                EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":temp.get("Individual Amount")})
                EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":temp.get("Individual Remaining")})
                EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate": calculate_difference(temp.get("Individual Amount"), temp.get("Individual Remaining"))})
        elif(x.get("Type")=="Deductible"):
            if(x.get("Category")=="General"): 
                EligibilityPatientVerification.update({"IndividualAnnualDeductible":temp.get("Individual Amount")})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":temp.get("Individual Used")})
                EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":calculate_difference(temp.get("Individual Amount"), temp.get("Individual Used"))})
                EligibilityPatientVerification.update({"FamilyAnnualDeductible":temp.get("Family Amount")})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":temp.get("Family Used")})
                EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":calculate_difference(temp.get("Family Amount"), temp.get("Family Used"))})
            EligibilityDeductiblesProcCode.append(temp)

    
    
    Limitation_dict={}
    for x in data.get("EligibilityOtherProvisions")[0].get("ExclusionsAndLimitations")[1:]:
        Limitation_dict.update({x.get("Category"):x.get("ExclusionsAndLimitations")})



    for benefits in EligibilityBenefitsData:
        benefitsPercent = ""
        limitation = ""
        Type = ""
        ammount = ""
        deductiblesApply = ""
        history = ""
        if (benefits.get("Proccode") == benefits.get("procedureCode")):
            if (benefits.get("procedureCovered") != "Not Covered"):
                benefitsPercent = benefits.get("procedureCovered")
            limitation = Limitation_dict.get(benefits.get("procedure"))
            Type = benefits.get("procedure")
            ammount = benefits.get("SubProcedureName")
            if("Prophylaxis" in benefits.get("SubProcedureName") and "Prophylaxes" in limitation):
                for limNew in limitation.split("."):
                    if "Prophylaxes" in limNew:
                        limitation = limNew.strip()
                        break
            if("Fluoride" in benefits.get("SubProcedureName") and "Fluoride" in limitation):
                for limNew in limitation.split("."):
                    if "Fluoride" in limNew:
                        limitation = limNew.strip()
                        break
            if("Space" in benefits.get("SubProcedureName") and "Space" in limitation):
                for limNew in limitation.split("."):
                    if "Space" in limNew:
                        limitation = limNew.strip()
                        break
            if("Composites" in benefits.get("SubProcedureName") and "composite" in limitation):
                for limNew in limitation.split("."):
                    if "composite" in limNew:
                        limitation = limNew.strip()
                        break
            if("Crowns" in benefits.get("SubProcedureName") and "crowns" in limitation):
                for limNew in limitation.split("."):
                    if "crowns" in limNew:
                        limitation = limNew.strip()
                        break
            for deductCodes in EligibilityDeductiblesProcCodeData[0]:
                if (benefits.get("Proccode") in EligibilityDeductiblesProcCodeData[0].get(deductCodes)):
                    deductiblesApply = "Yes"
                    break
                else:
                    deductiblesApply = "No"

            for hist in EligibilityTreatmentHistory:
                if (hist.get("Procedures") in benefits.get("SubProcedureName") or hist.get("Procedures") in limitation):
                    history = hist.get("ServiceDates")

            if(("D2391" or "D2392" or "D2393" or "D2394") in benefits.get("procedureCode")):
                EligibilityPatientVerification.update({"AlternativeBenefitProvision":"No"})
        
        if benefitsPercent == "":
            continue
        
        EligibilityBenefits.append({
            "ProcedureCode": benefits.get("Proccode"),
            "ProcedureCodeDescription": procCodeDesc.get(benefits.get("Proccode")),
            "Amount": "",
            "Type": Type,
            "limitation": limitation,
            "DeductibleApplies": deductiblesApply,
            "Copay": "",
            "Benefits": benefitsPercent
        })

        if (history != ""):
            EligibilityServiceTreatmentHistory.append({
                "ProcedureCode": benefits.get("Proccode"),
                "LimitationText": limitation,
                "History": history,
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": procCodeDesc.get(benefits.get("Proccode"))
            })
            TreatmentHistorySummary.append({
                "ProcedureCode": benefits.get("Proccode"),
                "LimitationText": limitation,
                "History": history,
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": "",
                "ProcedureCodeDescription": procCodeDesc.get(benefits.get("Proccode"))
            })
    
    
    # EligibilityServiceTreatmentHistory=[]
    # for x in data.get("EligibilityServiceTreatmentHistory")[1:]:
    #     temp={}
    #     tempmapdict={
    #         "ProcedureCode": "D0120",
    #         "ProcedureCodeDescription": "Periodic oral evaluation - established patient",
    #         "LimitationText": "Benefit is limited to two of any oral evaluation procedure within the contract period. Comprehensive evaluations are limited to once per provider.",
    #         "LimitationAlsoAppliesTo": "D0145, D0150, D0160, D0180, D0190, D0191, D9310",
    #         "ServiceDate": "12/09/2022, 06/24/2022, 12/17/2021, 07/05/2021, 01/04/2021, 07/24/2020, 01/03/2020, 07/26/2019, 12/21/2018, 05/25/2018, 11/21/2017",
    #         "ToothCode": "",
    #         "ToothDescription": "",
    #         "ToothSurface": ""
    #     }
    #     temp=mapdicts(tempmapdict, temp)
    #     temp.update({"ProcedureCodeDescription":x.get("Procedures"), "Eligible":x.get("Eligible")})
    #     EligibilityServiceTreatmentHistory.append(temp)
    
    # EligibilityBenefits=[]
    # Limitation_dict={}
    # for x in data.get("EligibilityOtherProvisions")[0].get("ExclusionsAndLimitations")[1:]:
    #     temp={}
    #     Limitation_dict.update({x.get("Category"):x.get("ExclusionsAndLimitations")})
    #     temp.update({"Category":x.get("Category"), "limitation":x.get("ExclusionsAndLimitations")})
    #     # EligibilityBenefits.append(temp)
    
    # EligibilityAgeLimitation=[]
    # temp=data.get("EligibilityAgeLimitation")[0].get("AgeLimitations")
    # temp=temp.replace("Overage Dependent Options", "")
    # while "\n\n" in temp: 
    #     temp=temp.replace("\n\n", "\n")
    # temp=temp.split("\n")[2:]
    # count=0
    # OverageDependentOptions={}
    # while count<len(temp):
    #     if(":" not in temp[count]):
    #         EligibilityAgeLimitation.append({"Name":temp[count], "Age":temp[count+1], "Rule":temp[count+2]})
    #         count+=3
    #     else:
    #         t=temp[count].index(":")
    #         OverageDependentOptions.update({temp[count][:t]:temp[count][t+1:]})
    #         count+=1
    # for x in data.get("EligibilityBenefits"):
    #     temp={}
    #     tempmapdict={
    #         "procedureCode": "D0120",
    #         "procedureCodeDescription": "Periodic oral evaluation - established patient",
    #         "limitation": "Benefit is limited to two of any oral evaluation procedure within the contract period. Comprehensive evaluations are limited to once per provider.",
    #         "PreApproval": "No",
    #         "DeductibleApplicable": "No"
    #     }
    #     temp=mapdicts(tempmapdict, temp)
    #     temp.update({"limitation":Limitation_dict.get(x.get("procedure"))})
    #     temp.update({"Category":x.get("SubProcedureName")})
    #     temp.update({"procedureCodeDescription":procCodeDesc.get(x.get("procedureCode"))})
    #     temp.update(x)
    #     EligibilityBenefits.append(temp)
    
    
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    for x in data.get("EligibilityMaximums"):
        if(x.get('Type')=="Maximum"):

            templist=x.get("Individual").split()
            EligibilityMaximums.append({
                "Type":f"{x.get('Type')}s",
                "Network":"Delta Dental PPO",
                "Amount":templist[1],
                "Remaining":templist[-1],
                "ServiceCategory":x.get("Category"),
                "Family_Individual":"Individual"
            })

            templist=x.get("Family").split()
            EligibilityMaximums.append({
            "Type":f"{x.get('Type')}s",
            "Network":"Delta Dental PPO",
            "Amount":templist[1],
            "Remaining":templist[-1],
            "ServiceCategory":x.get("Category"),
            "Family_Individual":"Family"
        })

        elif(x.get('Type')=="Deductible"):

            templist=x.get("Individual").split()
            EligibilityDeductiblesProcCode.append({
                "Type":f"{x.get('Type')}s",
                "Network":"Delta Dental PPO",
                "Amount":templist[1],
                "Remaining":templist[-1],
                "ServiceCategory":x.get("Category"),
                "Family_Individual":"Individual"
            })

            templist=x.get("Family").split()
            EligibilityDeductiblesProcCode.append({
            "Type":f"{x.get('Type')}s",
            "Network":"Delta Dental PPO",
            "Amount":templist[1],
            "Remaining":templist[-1],
            "ServiceCategory":x.get("Category"),
            "Family_Individual":"Family"
        })

    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":changeNone(EligibilityPatientVerification.get("PlanType"))})
        
    output={}
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "","AgeLimit": ""}]})
    
    data=output
    output={}
    for x in data:
        temp1=[]
        for y in data.get(x):
            temp2={}
            for z in y:
                temp2.update({z.replace(")", "_").replace("(", "_"):y.get(z)})
                # del y[z]
            temp1.append(temp2)
        output.update({x:temp1})
    return output

# request=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\delta dental ohio\dev\SD%20Payor%20Scraping\deltadentalohio.json", 'r'))
# data=json.load(open(r"C:\Users\iamha\Desktop\BPK teck\All Payors\SDB EXTERNAL\delta dental ohio\dev\SD%20Payor%20Scraping\output.json", 'r'))
# output=main(data, request)
# with open("tootlKitRES.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)
