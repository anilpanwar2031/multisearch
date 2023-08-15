from mapPDF import mapEligibilityPatientVerification
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
def main(data):

    EligibilityPatientVerification=mapEligibilityPatientVerification()
    try:
        temp=data.get("EligibilityPatientVerification")[0]
        EligibilityPatientVerification.update({"FamilyMemberName":temp.get("Patient")})
        EligibilityPatientVerification.update({"FamilyMemberDateOfBirth":temp.get("DOB")})
        network=temp.get("Product Type")
        EligibilityPatientVerification.update({"PlanType":network})
        EligibilityPatientVerification.update({"InsuranceFeeScheduleUsed":temp.get("Product Type")})
        EligibilityPatientVerification.update({"PlanNumber":temp.get("Product ID")})
        EligibilityPatientVerification.update({"GroupNumber":temp.get("Group ID")})
        EligibilityPatientVerification.update({"GroupName":temp.get("Group Name")})
        EligibilityPatientVerification.update({"InsuranceName":temp.get("Product Line")})
        EligibilityPatientVerification.update({"FamilyMemberEffectiveDate":temp.get("Effective Date")})
        if(temp.get("Eligible")=="Y"):
            EligibilityPatientVerification.update({"EligibilityStatus":"Active"})
        EligibilityPatientVerification.update({"FamilyMemberEndDate":temp.get("Term Date")})
        EligibilityPatientVerification.update({"ClaimMailingAddress":temp.get("Claims Address")})
        EligibilityPatientVerification.update({"ClaimsAddress":temp.get("Claims Address")})
        EligibilityPatientVerification.update({"ClaimPayerID":temp.get("Payor Id")})

        EligibilityPatientVerification.update({"Address":temp.get("Address").replace("\n", " ")})
        EligibilityPatientVerification.update({"Relationship":temp.get("Relationship")})
        EligibilityPatientVerification.update({"Spoken Language":temp.get("Spoken Language")})
        EligibilityPatientVerification.update({"Language Assistance":temp.get("Language Assistance")})
        EligibilityPatientVerification.update({"Provider Network Status":temp.get("Provider Network Status")})
        EligibilityPatientVerification.update({"Subscriber ID":temp.get("Subscriber ID")})
        EligibilityPatientVerification.update({"Plan Year Begins":temp.get("Plan Year Begins")})
        EligibilityPatientVerification.update({"Essential Health Benefits":temp.get("Essential Health Benefits")})
        EligibilityPatientVerification.update({"Product Description":temp.get("Product Description")})
        EligibilityPatientVerification.update({"Provider Location":temp.get("Provider Location").replace("\n", " ")})
        EligibilityPatientVerification.update({"Assignment Status":temp.get("Assignment Status")})




    except: pass
    EligibilityBenefits=[]
    TreatmentHistorySummary=[]
    CoverageAndDeductible={}
    try:
        for x in data.get("EligibilityOtherProvisions"):
            CoverageAndDeductible.update({
                x.get("Procedure Category"):
                {
                    "DeductibleApplies":x.get("Deductible Applies", "").replace("N", "No").replace("Y", "Yes"),
                    "Benefits":x.get("Coverage(IN)")
                }
            })

            if "PREVENTIVE" in x.get("Procedure Category Description"):
                EligibilityPatientVerification.update({"FamilyMemberWaitingPeriod":x.get("Waiting Period Met Date")})

    except: pass
    
    try:
        for x in data.get("EligibilityBenefits"):

            # alternativebenefits
            proccode = x.get("ADA Code")
            alternatebenefit = x.get("Alternate Benefit")
            
            if 'D2391' in proccode:
                if 'D2140' in alternatebenefit:
                    EligibilityPatientVerification.update({"AlternativeBenefitProvision":'Yes'})
                else:
                    EligibilityPatientVerification.update({"AlternativeBenefitProvision":'No'})  

                

            try:
                DeductibleApplies=CoverageAndDeductible.get(x.get("Procedure Category")).get("DeductibleApplies")
            except: DeductibleApplies=""
            try:
                Benefits=CoverageAndDeductible.get(x.get("Procedure Category")).get("Benefits")
            except: 
                Benefits=""
            EligibilityBenefits.append({
                "ProcedureCode": x.get("ADA Code", ""),
                "ProcedureCodeDescription": x.get("ADA Description", ""),
                "Amount": "",
                "limitation": x.get("Service Date Procedure Code Frequency* (i-ii-iii)", "") +', '+ x.get("Age Limit"),
                "DeductibleApplies": DeductibleApplies,
                "Copay": "",
                "Benefits": Benefits
            })
            temp=x.get("Service Date 1", "").replace("-", "")+' '+x.get("Service Date 2", "").replace("-", "")+' '+x.get("Service Date 3", "").replace("-", "")+' '+x.get("Service Date 4", "").replace("-", "")
            temp=temp.strip()
            
            TreatmentHistorySummary.append({
                "ProcedureCode": x.get("ADA Code", ""),
                "LimitationText": x.get("Service Date Procedure Code Frequency* (i-ii-iii)", ""),
                "History": temp,
                "Tooth": "",
                "Surface": "",
                "LimitationAlsoAppliesTo": x.get("Related Codes", ""),
                "ProcedureCodeDescription": x.get("ADA Description", "")
            })
    except Exception as e:
        print(e)
   


    EligibilityServiceTreatmentHistory=TreatmentHistorySummary
    EligibilityMaximums, EligibilityDeductibles=[], []
    try:
        temp=data.get("EligibilityMaximums")[0]
        IndividualAnnualMaximumBenefits=getsum(temp.get("Annual Maximium Benefits Remaining").replace("Remaining","").strip(),temp.get("Annual Maximium Benefits used").replace("Used to Date","").strip())
        IndividualAnnualBenefitsUsedtoDate=temp.get("Annual Maximium Benefits used").replace("Used to Date","").strip()
        IndividualAnnualRemainingBenefit=temp.get("Annual Maximium Benefits Remaining", "").replace("Remaining","").strip()
        OrthodonticLifetimeBenefit=temp.get("Lifetime Maximum Benefits - Orthodontics").split(' ')[-1].replace(",", "")
        OrthodonticLifetimeBenefitUsedtoDate=temp.get("Lifetime Maximum Benefits - Orthodontics").split(' ')[0]
        OrthodonticLifetimeRemainingBenefit=calculate_difference(temp.get("Lifetime Maximum Benefits - Orthodontics").split(' ')[-1], temp.get("Lifetime Maximum Benefits - Orthodontics").split(' ')[0])
        IndividualAnnualDeductible=temp.get("Deductible").split(' ')[-1].replace(",", "")
        IndividualAnnualDeductibleMet=temp.get("Deductible").split(' ')[0]
        IndividualAnnualDeductibleRemaining=calculate_difference(temp.get("Deductible").split(' ')[-1], temp.get("Deductible").split(' ')[0])
        FamilyAnnualDeductible="0.0"
        FamilyAnnualDeductibleMet="0.0"
        FamilyAnnualDeductibleRemaining="0.0"
        EligibilityMaximums=[
            {"Type": "Annual Maximum",
            "Network": network,
            "Amount": getsum(temp.get("Annual Maximium Benefits Remaining").replace("Remaining","").strip(),temp.get("Annual Maximium Benefits used").replace("Used to Date","").strip()),
            "Remaining": temp.get("Annual Maximium Benefits Remaining", "").replace("Remaining","").strip(),
            "ServiceCategory": "Dental",
            "Family_Individual": "Individual"
            },
            {
            "Type": "Lifetime Maximum",
            "Network": network,
            "Amount": temp.get("Lifetime Maximum Benefits - Orthodontics").split(' ')[-1].replace(",", ""),
            "Remaining": calculate_difference(temp.get("Lifetime Maximum Benefits - Orthodontics").split(' ')[-1], temp.get("Lifetime Maximum Benefits - Orthodontics").split(' ')[0]),
            "ServiceCategory": "Orthodontics",
            "Family_Individual": "Individual"
            }
        ]
        EligibilityDeductibles=[
            {"Type": "Annual Deductibles",
            "Network": network,
            "Amount": temp.get("Deductible").split(' ')[-1].replace(",", ""),
            "Remaining": calculate_difference(temp.get("Deductible").split(' ')[-1], temp.get("Deductible").split(' ')[0]),
            "ServiceCategory": "Dental",
            "Family_Individual": "Individual"
            }
        ]
    except: pass
    try:
        EligibilityPatientVerification.update({"IndividualAnnualMaximumBenefits":IndividualAnnualMaximumBenefits})
        EligibilityPatientVerification.update({"IndividualAnnualBenefitsUsedtoDate":IndividualAnnualBenefitsUsedtoDate})
        EligibilityPatientVerification.update({"IndividualAnnualRemainingBenefit":IndividualAnnualRemainingBenefit})
        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefit":OrthodonticLifetimeBenefit})
        EligibilityPatientVerification.update({"OrthodonticLifetimeBenefitUsedtoDate":OrthodonticLifetimeBenefitUsedtoDate})
        EligibilityPatientVerification.update({"OrthodonticLifetimeRemainingBenefit":OrthodonticLifetimeRemainingBenefit})
        EligibilityPatientVerification.update({"IndividualAnnualDeductible":IndividualAnnualDeductible})
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleMet":IndividualAnnualDeductibleMet})
        EligibilityPatientVerification.update({"IndividualAnnualDeductibleRemaining":IndividualAnnualDeductibleRemaining})
        # FamilyAnnualDeductible=IndividualAnnualDeductible
        # FamilyAnnualDeductibleMet=IndividualAnnualDeductibleMet
        # FamilyAnnualDeductibleRemaining=IndividualAnnualDeductibleRemaining
        # EligibilityPatientVerification.update({"FamilyAnnualDeductible":FamilyAnnualDeductible})
        # EligibilityPatientVerification.update({"FamilyAnnualDeductibleMet":FamilyAnnualDeductibleMet})
        # EligibilityPatientVerification.update({"FamilyAnnualDeductibleRemaining":FamilyAnnualDeductibleRemaining})
    except: pass
    EligibilityPatientVerification.update({"oonBenefits":"No"})
    output={}
    
    output.update({"EligibilityPatientVerification":[EligibilityPatientVerification]})
    output.update({"EligibilityBenefits":EligibilityBenefits})
    output.update({"EligibilityMaximums":EligibilityMaximums})
    output.update({"EligibilityDeductiblesProcCode":EligibilityDeductibles})
    output.update({"EligibilityServiceTreatmentHistory":EligibilityServiceTreatmentHistory})
    output.update({"TreatmentHistorySummary":TreatmentHistorySummary})
    output.update({"EligibilityAgeLimitation":[{"FamilyMember": "", "AgeLimit": ""}]})
    # data=output
    # output={}
    # for x in data:
    #     temp1=[]
    #     for y in data.get(x):
    #         temp2={}
    #         for z in y:
    #             temp2.update({z.replace(")", "_").replace("(", "_"):y.get(z)})
    #             # del y[z]
    #         temp1.append(temp2)
    #     output.update({x:temp1})
    return output

    

# data=json.load(open(r"C:\Users\saran\Downloads\output5uhc.json", 'r'))
# output=main(data)
# with open("UHCres3.json", "w") as outfile:
#     json.dump(output, outfile, indent=4)