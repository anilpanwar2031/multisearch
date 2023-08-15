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
def main(Scraperdata, request):
    patientdata = request.get("PatientData")[0]
    EligibilityPatient = Scraperdata.get("EligibilityPatientVerification")[0]
    EligibilityMaximiums = Scraperdata.get("EligibilityMaximums")
    EligibilityBenefitsData = Scraperdata.get("EligibilityBenefits")

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    EligibilityMaximums=[]
    EligibilityDeductiblesProcCode=[]
    EligibilityServiceTreatmentHistory=[]
    TreatmentHistorySummary=[]
    EligibilityBenefits=[]

    if EligibilityPatient.get("Effective Date", None):
        EligibilityPatientVerification.update({"EligibilityStatus":"Active"})

    EligibilityPatientVerification.update({"FamilyMemberId":patientdata.get("SubscriberId")})
    EligibilityPatientVerification.update({"SubscriberName":EligibilityPatient.get("Member Name first name")+" "+EligibilityPatient.get("Member Name last name")})
    EligibilityPatientVerification.update({"FamilyMemberName":EligibilityPatient.get("Dependent Name")})
    EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":patientdata.get("BirthDate")})
    EligibilityPatientVerification.update({"ClaimMailingAddress":EligibilityPatient.get("ClaimMailingAddress").replace("Please mail claims and predeterminations to: ", "")})
    EligibilityPatientVerification.update({"ClaimsAddress":EligibilityPatient.get("ClaimMailingAddress").replace("Please mail claims and predeterminations to: ", "")})
    payorID = EligibilityPatient.get("PayorID").split("#")
    EligibilityPatientVerification.update({"ClaimPayerID":payorID[1].replace(".", "").replace(" ", "")})
    EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":EligibilityPatient.get("Effective Date")})
    EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":EligibilityPatient.get("Network Name")})
    EligibilityPatientVerification.update({"GroupName":EligibilityPatient.get("Employer")})
    EligibilityPatientVerification.update({"GroupNumber":EligibilityPatient.get("Employer Number")})
    EligibilityPatientVerification.update({"MissingToothClause":"A missing tooth clause applies to services such as the initial placement of full or partial dentures, fixed bridges, implants, and implant crowns. These services are only covered if the natural teeth being replaced were extracted while covered under this plan"})
    EligibilityPatientVerification.update({"DependentChildCoveredAgeLimit":"Dependent dental will be terminated when dependent has turned 26 years old"})
    EligibilityPatientVerification.update({"CoordinationofBenefits":"Yes"})
    EligibilityPatientVerification.update({"BenefitPeriod":EligibilityPatient.get("Benefit Period")})
    EligibilityPatientVerification.update({"InNetworkOutNetwork":"The patient should see an In Network dentist for the best benefit, Lesser benefits are available by visiting a non-participating dentist"})
    EligibilityPatientVerification.update({"oonBenefits":"Yes"})
    EligibilityPatientVerification.update({"AlternativeBenefitProvision":"Composites are considered for posterior teeth which includes molars and pre-molars (bicuspids)"})
    EligibilityPatientVerification.update({"OrthodonticAgeLimits":"if the bands/appliances were placed prior to age 19"})
    EligibilityPatientVerification.update({"PreCertRequired":"No"})
    EligibilityPatientVerification.update({"PreauthorizationRequired":"No"})
    EligibilityPatientVerification.update({"CoordinationofBenefitsType":"Standard/Birthday Rule as defined by NAIC"})
    EligibilityPatientVerification.update({"HowareBenefitsPaid":"The benefit for the initial fee is 25% of the lifetime maximum or the total fee, whichever is less"})
    EligibilityPatientVerification.update({"TreatmentinProgressCoverage":"There are no benefits payable if the appliance or bands were placed prior to the effective date, unless treatment was in progress under prior group orthodontic coverage, and no lapse in coverage"})
    EligibilityPatientVerification.update({"AutomaticPayments":"Yes"})
    EligibilityPatientVerification.update({"ContinuationClaimNeeded":"No"})

    ###ElgibilityMaximiums
    for item in EligibilityMaximiums:
        if item.get("InNetwork", None):
            if item.get("InNetwork") == "Calendar Year Maximum":
                if item.get("Orthodontia") != "None":
                    try:
                        lifetimeMaximiums = item.get("Orthodontia").split("$")
                        EligibilityPatientVerification.update({"IndividualLifetimeMaximumBenefits":"$"+lifetimeMaximiums[1].replace("Remaining ", "").replace("\n", "")})
                        EligibilityPatientVerification.update({"IndividualLifetimeRemainingBenefit":"$"+lifetimeMaximiums[2]})
                        EligibilityPatientVerification.update({"IndividualLifetimeBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit").strip())})
                        #---Orthodontics lifetime
                        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":"$"+lifetimeMaximiums[1].replace("Remaining ", "").replace("\n", "")})
                        EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":"$"+lifetimeMaximiums[2]})
                        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualLifetimeRemainingBenefit").strip())})
                    except:
                        pass
                if item.get("Basic") != "None":
                    try:
                        FamilyAnnualMaximumBenefitsData = item.get("Basic").split("$")
                        EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":"$"+FamilyAnnualMaximumBenefitsData[1].replace("Remaining ", "").replace("\n", "")})
                        EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":"$"+FamilyAnnualMaximumBenefitsData[2].replace(" Rollover Amount Remaining ", "")})
                        EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualMaximumBenefits").strip(),EligibilityPatientVerification.get("IndividualAnnualRemainingBenefit").strip())})
                    except:
                        pass
            if item.get("InNetwork") == "Family Deductible":
                if item.get("Orthodontia") != "None":
                    try:
                        FamilyLifetimeDeductibleData = item.get("Orthodontia").split("$")
                        EligibilityPatientVerification.update({"FamilyLifetimeDeductible":"$"+FamilyLifetimeDeductibleData[1].replace("Remaining ", "").replace("\n", "")})
                        EligibilityPatientVerification.update({"FamilyLifetimeRemainingDeductible":"$"+FamilyLifetimeDeductibleData[2]})
                        EligibilityPatientVerification.update({"FamilyLifetimeDeductibleMet":calculate_difference(EligibilityPatientVerification.get("FamilyLifetimeDeductible").strip(),EligibilityPatientVerification.get("FamilyLifetimeRemainingDeductible").strip())})
                    except:
                        pass
                if item.get("Basic") != "None":
                    try:
                        FamilyAnnualDeductibleData = item.get("Basic").split("$")
                        EligibilityPatientVerification.update({"FamilyAnnualDeductible":"$"+FamilyAnnualDeductibleData[1].replace("Remaining ", "").replace("\n", "")})
                        EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":"$"+FamilyAnnualDeductibleData[2]})
                        EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("FamilyAnnualDeductible").strip(),EligibilityPatientVerification.get("FamilyAnnualDeductibleRemaining").strip())})
                    except:
                        pass
            if item.get("InNetwork") == "Calendar Year Individual Deductible":
                if item.get("Orthodontia") != "None":
                    try:
                        IndividualLifetimeDeductibleData = item.get("Orthodontia").split("$")
                        EligibilityPatientVerification.update({"IndividualLifetimeDeductible":"$"+IndividualLifetimeDeductibleData[1].replace("Remaining ", "").replace("\n", "")})
                        EligibilityPatientVerification.update({"IndividualLifetimeRemainingDeductible":"$"+IndividualLifetimeDeductibleData[2]})
                        EligibilityPatientVerification.update({"IndividualLifetimeDeductibleMet":calculate_difference(EligibilityPatientVerification.get("IndividualLifetimeDeductible").strip(),EligibilityPatientVerification.get("IndividualLifetimeRemainingDeductible").strip())})
                    except:
                        pass
                if item.get("Basic") != "None":
                    try:
                        IndividualAnnualDeductibleData = item.get("Basic").split("$")
                        EligibilityPatientVerification.update({"IndividualAnnualDeductible":"$"+IndividualAnnualDeductibleData[1].replace("Remaining ", "").replace("\n", "")})
                        EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":"$"+IndividualAnnualDeductibleData[2]})
                        EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":calculate_difference(EligibilityPatientVerification.get("IndividualAnnualDeductible").strip(),EligibilityPatientVerification.get("IndividualAnnualDeductibleRemaining").strip())})
                    except:
                        pass
            if item.get("InNetwork") == "Waiting Period":                
                    EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":item.get("Basic")})
            
    ####All-Maximiums
    EligibilityMaximumsTemp = []
    for Allitem in EligibilityMaximiums:
        if Allitem.get("InNetwork", None) and Allitem.get("InNetwork") != "Policy Pays" and Allitem.get("InNetwork") != "Waiting Period":
            if Allitem.get("Preventive", None):
                EligibilityMaximumsTemp.append({
                    "NetworkStatus": "In Network",
                    "Benefit": "Preventive",
                    "Type": Allitem.get("InNetwork"),
                    "Amount": Allitem.get("Preventive").strip()
                })
            if Allitem.get("Basic", None):
                EligibilityMaximumsTemp.append({
                    "NetworkStatus": "In Network",
                    "Benefit": "Basic",
                    "Type": Allitem.get("InNetwork"),
                    "Amount": Allitem.get("Basic").strip()
                })
            if Allitem.get("Major", None):
                EligibilityMaximumsTemp.append({
                    "NetworkStatus": "In Network",
                    "Benefit": "Major",
                    "Type": Allitem.get("InNetwork"),
                    "Amount": Allitem.get("Major").strip()
                })
            if Allitem.get("Orthodontia", None):
                EligibilityMaximumsTemp.append({
                    "NetworkStatus": "In Network",
                    "Benefit": "Orthodontia",
                    "Type": Allitem.get("InNetwork"),
                    "Amount": Allitem.get("Orthodontia").strip()
                })

        if Allitem.get("OutNetwork", None) and Allitem.get("OutNetwork") != "Policy Pays" and Allitem.get("OutNetwork") != "Waiting Period":
            if Allitem.get("Preventive", None):
                EligibilityMaximumsTemp.append({
                    "NetworkStatus": "Out of Network",
                    "Benefit": "Preventive",
                    "Type": Allitem.get("OutNetwork"),
                    "Amount": Allitem.get("Preventive").strip()
                })
            if Allitem.get("Basic", None):
                EligibilityMaximumsTemp.append({
                    "NetworkStatus": "Out of Network",
                    "Benefit": "Basic",
                    "Type": Allitem.get("OutNetwork"),
                    "Amount": Allitem.get("Basic").strip()
                })
            if Allitem.get("Major", None):
                EligibilityMaximumsTemp.append({
                    "NetworkStatus": "Out of Network",
                    "Benefit": "Major",
                    "Type": Allitem.get("OutNetwork"),
                    "Amount": Allitem.get("Major").strip()
                })
            if Allitem.get("Orthodontia", None):
                EligibilityMaximumsTemp.append({
                    "NetworkStatus": "Out of Network",
                    "Benefit": "Orthodontia",
                    "Type": Allitem.get("OutNetwork"),
                    "Amount": Allitem.get("Orthodontia").strip()
                })
    
    for new in EligibilityMaximumsTemp:
        # print('new1:-',new)
        splittBasic = new.get("Amount").split("$")
        # print('split1:-',splittBasic)
        if len(splittBasic) > 1:
            AmountBasic = "$"+splittBasic[1].replace("Remaining ", "").replace("\n", "")
            RemainingBasic = "$"+splittBasic[2]
        new.update({"Amount":AmountBasic})
        new.update({"Remaining":RemainingBasic.replace(" Rollover Amount Remaining ", "")})
        if search("Family", new.get("Type")):
            new.update({"Family_Individual":"Family"})
        else:
            new.update({"Family_Individual":"Individual"})
    
    for item in EligibilityMaximumsTemp:
        serviceCatgory = ""
        if item.get("Type") == "Calendar Year Maximum":
            serviceCatgory = "Orthodontics"
        else:
            serviceCatgory = "Dental"

        if search("Deductible", item.get("Type")):
            EligibilityDeductiblesProcCode.append({
                "Type": item.get("Type"),
                "Network": item.get("NetworkStatus"),
                "Amount": item.get("Amount"),
                "Remaining": item.get("Remaining"),
                "ServiceCategory": serviceCatgory,
                "Family_Individual": item.get("Family_Individual")
            })
        else:
            EligibilityMaximums.append({
                "Type": item.get("Type"),
                "Network": item.get("NetworkStatus"),
                "Amount": item.get("Amount"),
                "Remaining": item.get("Remaining"),
                "ServiceCategory": serviceCatgory,
                "Family_Individual": item.get("Family_Individual")
            })


    #procodesElgibilityBenefits
    for item in EligibilityBenefitsData:
        try:
            if item.get("Benefit Plan Details") == None or item.get("Benefit Plan Details") == "Benefit Plan Details":
                continue
            else:
                service = item.get("Service").split("D")
                unit = item.get("Benefit Plan Details").split("Policy Pays")
                if item.get("Code Allowance", None):
                    if "\u00a0" in item.get("Code Allowance"):
                        policyPays = unit[1].split("Frequency")
                        CodeAllowance = item.get("Code Allowance").split("\u00a0")
                        feeSchdule = CodeAllowance[3].split("Was")
                        EligibilityBenefits.append({
                            "ProcedureCode": CodeAllowance[1].replace("Code Allowance","").strip(),
                            "ProcedureCodeDescription": service[0].strip(),
                            "CodeAllowance": CodeAllowance[2].replace("Fee Schedule","").strip(),
                            "unit": unit[0].replace("Unit","").strip(),
                            "NetworkStatus": "In Network",
                            "Benefits": policyPays[0].strip(),
                            "limitation": policyPays[1].strip(),
                            "FeeSchedule": feeSchdule[0].strip(),
                            "ServiceHistory": item.get("Service History").replace(" ", " , ")
                        })
                    else:
                        CodeAllowance = item.get("Code Allowance").split("Select")
                        policyPays = unit[1].split("Frequency")
                        EligibilityBenefits.append({
                            "ProcedureCode": CodeAllowance[0].strip(),
                            "ProcedureCodeDescription": service[0].strip(),
                            "CodeAllowance": "N/A",
                            "unit": unit[0].replace("Unit","").strip(),
                            "NetworkStatus": "In Network",
                            "Benefits": policyPays[0].strip(),
                            "limitation": policyPays[1].strip(),
                            "FeeSchedule": "N/A",
                            "ServiceHistory": item.get("Service History").replace(" ", " , ")
                        })

                elif item.get("Service History", None):
                    policyPays = unit[1].split("Frequency")
                    if search("History", item.get("Service History")):
                        history = "No History"
                    else:
                        history = item.get("Service History")
                    for dcode in service[1:]:
                        EligibilityBenefits.append({
                            "ProcedureCode": "D"+dcode.replace(", ","").strip(),
                            "ProcedureCodeDescription": service[0].strip(),
                            "CodeAllowance": "N/A",
                            "unit": unit[0].replace("Unit","").strip(),
                            "NetworkStatus": "In Network",
                            "Benefits": policyPays[0].strip(),
                            "limitation": policyPays[1].strip(),
                            "FeeSchedule": "N/A",
                            "ServiceHistory": history
                        })
                else:
                    policyPays = unit[1]
                    for dcode in service[1:]:
                        EligibilityBenefits.append({
                            "ProcedureCode": "D"+dcode.replace(", ","").strip(),
                            "ProcedureCodeDescription": service[0].strip(),
                            "CodeAllowance": "N/A",
                            "unit": unit[0].replace("Unit","").strip(),
                            "NetworkStatus": "In Network",
                            "Benefits": policyPays.strip(),
                            "limitation": "N/A",
                            "FeeSchedule": "N/A",
                            "ServiceHistory": "No History"
                        })
        except:
            continue

    for unit in EligibilityBenefits:
        unit.update({"Copay":""})
        unit.update({"Amount":""})
        Preventive =""
        Basic =""
        Major =""
        Orthodontia =""
        for valDeduct in EligibilityMaximiums:
            if valDeduct.get("InNetwork") == "Calendar Year Individual Deductible":
                if valDeduct.get("Preventive"):
                    Preventive = valDeduct.get("Preventive").split("\n")[0].replace("Deductible","").strip()
                if valDeduct.get("Basic"):
                    Basic = valDeduct.get("Basic").split("\n")[0].replace("Deductible","").strip()
                if valDeduct.get("Major"):
                    Major = valDeduct.get("Major").split("\n")[0].replace("Deductible","").strip()
                try:
                    Orthodontia = valDeduct.get("Orthodontia").split("\n")[0].replace("Deductible","").strip()
                except:
                    pass
                
        if unit.get("unit") == "Preventive":
            if Preventive == "$0.00":
                unit.update({"DeductibleApplies":"No"})
            else:
                unit.update({"DeductibleApplies":"Yes"})
        elif unit.get("unit") == "Basic":
            if Basic == "$0.00":
                unit.update({"DeductibleApplies":"No"})
            else:
                unit.update({"DeductibleApplies":"Yes"})
        elif unit.get("unit") == "Major":
            if Major == "$0.00":
                unit.update({"DeductibleApplies":"No"})
            else:
                unit.update({"DeductibleApplies":"Yes"})
        elif unit.get("unit") == "Orthodontia":
            if Major == "$0.00":
                unit.update({"DeductibleApplies":"No"})
            else:
                unit.update({"DeductibleApplies":"Yes"})
        else:
            unit.update({"DeductibleApplies":"No"})

        if search("No", str(unit.get("ServiceHistory"))):
            unit.update({"ServiceHistory":unit.get("ServiceHistory").replace(" ,", "")})


    for item in EligibilityBenefits:
        EligibilityServiceTreatmentHistory.append({
            "ProcedureCode": item.get("ProcedureCode"),
            "LimitationText": item.get("limitation"),
            "History": item.get("ServiceHistory"),
            "Tooth": "",
            "Surface": "",
            "LimitationAlsoAppliesTo": "",
            "ProcedureCodeDescription": item.get("ProcedureCodeDescription")
        })
                    
    allcodeslist1 = ""
    EligibilityBenefits1 =[]
    for dictionary  in EligibilityBenefits:
        if dictionary.get("ProcedureCode") in allcodeslist1:
            # for historyitems in EligibilityBenefits1:
            #     if dictionary.get("ProcedureCode") in historyitems.get("ProcedureCode"):
            #         historyitems.update({"History":historyitems.get("History")+", "+dictionary['History']})
            #         break
            continue
        EligibilityBenefits1.append(dictionary)
        allcodeslist1 = allcodeslist1 +" "+dictionary['ProcedureCode']

    EligibilityBenefits = EligibilityBenefits1



    allcodeslist = ""
    EligibilityServiceTreatmentHistory1 =[]
    for dictionary  in EligibilityServiceTreatmentHistory:
        if dictionary.get("ProcedureCode") in allcodeslist:
            # for historyitems in EligibilityServiceTreatmentHistory1:
            #     if dictionary.get("ProcedureCode") in historyitems.get("ProcedureCode"):
            #         historyitems.update({"History":historyitems.get("History")+", "+dictionary['History']})
            #         break
            continue
        EligibilityServiceTreatmentHistory1.append(dictionary)
        allcodeslist = allcodeslist +" "+dictionary['ProcedureCode']

    EligibilityServiceTreatmentHistory = EligibilityServiceTreatmentHistory1
    
    

    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductiblesProcCode})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":EligibilityServiceTreatmentHistory})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    return output


